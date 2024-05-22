import typing
from pycom import bus, byte, component, controller, memory, program_counter, register


class Computer(component.Component):
    @classmethod
    def _controller_entries(cls) -> frozenset[controller.Controller.Entry]:

        def step(*controls: str) -> list[str]:
            return list(controls)

        def steps(*steps: list[str]) -> list[list[str]]:
            return list(steps)

        def entries(
            instruction: typing.Optional[int],
            starting_instruction_counter: int,
            reset_instruction_counter: bool,
            *steps: list[str],
        ) -> frozenset[controller.Controller.Entry]:
            steps_list: list[list[str]] = list(steps)
            reset_control = "controller.instruction_counter.reset"
            increment_control = "controller.instruction_counter.increment"
            last_control = (
                reset_control if reset_instruction_counter else increment_control
            )
            if not steps_list:
                steps_list = [[last_control]]
            else:
                for step in steps_list[:-1]:
                    if increment_control not in step:
                        step.append(increment_control)
                if last_control not in steps_list[-1]:
                    steps_list[-1].append(last_control)
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

        def load_from_pc(dest: str) -> list[list[str]]:
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

        def load_addr_at_pc() -> list[list[str]]:
            return steps(
                *load_from_pc("controller.address_buffer.in"),
                *load_from_pc("memory.address_low_byte.in"),
                step(
                    "controller.address_buffer.out",
                    "memory.address_high_byte.in",
                ),
            )

        def load_from_addr_at_pc(dest: str) -> list[list[str]]:
            return steps(
                *load_addr_at_pc(),
                step(
                    "memory.out",
                    dest,
                ),
            )

        def store_to_addr_at_pc(source: str) -> list[list[str]]:
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
            *load_from_pc("controller.instruction_buffer.in"),
        )

        def instruction(
            instruction: int,
            *steps: list[str],
        ) -> frozenset[controller.Controller.Entry]:
            return entries(
                instruction,
                len(preamble),
                True,
                *steps,
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
