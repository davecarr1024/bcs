import typing
from pycom import bus, byte, component, controller, memory, program_counter, register


class Computer(component.Component):
    @classmethod
    def _controller_entries(cls) -> frozenset[controller.Controller.Entry]:
        def step(*controls: str) -> frozenset[str]:
            return frozenset(controls)

        def steps(*steps: frozenset[str]) -> list[frozenset[str]]:
            return list(steps)

        def entries(
            instruction: typing.Optional[int],
            starting_instruction_counter: int,
            reset_instruction_counter: bool,
            steps: list[frozenset[str]],
        ) -> frozenset[controller.Controller.Entry]:
            reset_control = "controller.instruction_counter.reset"
            increment_control = "controller.instruction_counter.increment"
            last_control = (
                reset_control if reset_instruction_counter else increment_control
            )
            steps_list = [set(step) for step in steps] or [{last_control}]
            for step in steps_list[:-1]:
                step |= {increment_control}
            steps_list[-1] |= {last_control}
            return frozenset(
                {
                    controller.Controller.Entry.build(
                        instruction,
                        instruction_counter + starting_instruction_counter,
                        *step,
                    )
                    for instruction_counter, step in enumerate(steps_list)
                }
            )

        def load_from_pc(dest: str) -> list[frozenset[str]]:
            return steps(
                step(
                    "program_counter.high_byte.out",
                    "memory.address_high_byte.in",
                ),
                step(
                    "program_counter.low_byte.out",
                    "memory.address_low_byte.in",
                ),
                step(
                    "memory.out",
                    "program_counter.increment",
                    dest,
                ),
            )

        def load_addr_at_pc() -> list[frozenset[str]]:
            return steps(
                *load_from_pc("controller.address_buffer.in"),
                *load_from_pc("memory.address_low_byte.in"),
                step(
                    "controller.address_buffer.out",
                    "memory.address_high_byte.in",
                ),
            )

        def load_from_addr_at_pc(dest: str) -> list[frozenset[str]]:
            return steps(
                *load_addr_at_pc(),
                step(
                    "memory.out",
                    dest,
                ),
            )

        def store_to_addr_at_pc(source: str) -> list[frozenset[str]]:
            return steps(
                *load_addr_at_pc(),
                step(
                    source,
                    "memory.in",
                ),
            )

        preamble = entries(
            None,
            0,
            False,
            load_from_pc("controller.instruction_buffer.in"),
        )

        def instruction(
            instruction: int,
            *steps: frozenset[str],
        ) -> frozenset[controller.Controller.Entry]:
            return entries(
                instruction,
                len(preamble),
                True,
                list(steps),
            )

        return frozenset.union(
            preamble,
            # nop
            instruction(0x00),
            # lda immediate
            instruction(
                0x01,
                *load_from_pc("a.in"),
            ),
            # lda mem
            instruction(
                0x02,
                *load_from_addr_at_pc("a.in"),
            ),
            # sta mem
            instruction(
                0x03,
                *store_to_addr_at_pc("a.out"),
            ),
        )

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        data: typing.Optional[typing.Mapping[int, byte.Byte]] = None,
    ) -> None:
        self.bus = bus.Bus()
        self.a = register.Register(self.bus, "a")
        self.instruction_buffer = register.Register(self.bus, "instruction_buffer")
        self.memory = memory.Memory(self.bus, data=data)
        self.program_counter = program_counter.ProgramCounter(self.bus)
        self.controller = controller.Controller(self.bus, self._controller_entries())
        super().__init__(
            name or "computer",
            children=frozenset(
                {
                    self.a,
                    self.instruction_buffer,
                    self.memory,
                    self.program_counter,
                    self.controller,
                }
            ),
        )

    @typing.override
    def _str_line(self) -> str:
        return f"Computer(bus={self.bus})"

    def update(self) -> None:
        self.controller.apply()
        super().update()
