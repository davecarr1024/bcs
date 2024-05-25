import dataclasses
import enum
import typing
from pycom import (
    alu,
    bus,
    component,
    controller,
    memory,
    program_counter,
    register,
)


class Computer(component.Component):
    class Opcode(enum.Enum):
        NOP = 0xEA
        LDA_IMMEDIATE = 0xA9
        LDA_ABSOLUTE = 0xAD
        STA_ABSOLUTE = 0x8D
        SEC = 0x38
        CLC = 0x18
        ADC_IMMEDIATE = 0x69

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
                    controller.Controller.Entry(
                        instruction=instruction,
                        instruction_counter=instruction_counter
                        + starting_instruction_counter,
                        controls=frozenset(step),
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
            opcode: Computer.Opcode,
            *steps: frozenset[str],
        ) -> frozenset[controller.Controller.Entry]:
            return preamble | entries(
                opcode.value,
                len(preamble),
                True,
                list(steps),
            )

        return frozenset.union(
            instruction(cls.Opcode.NOP),
            instruction(
                cls.Opcode.LDA_IMMEDIATE,
                *load_from_pc("a.in"),
            ),
            instruction(
                cls.Opcode.LDA_ABSOLUTE,
                *load_from_addr_at_pc("a.in"),
            ),
            instruction(
                cls.Opcode.STA_ABSOLUTE,
                *store_to_addr_at_pc("a.out"),
            ),
            instruction(
                cls.Opcode.CLC,
                step(
                    "alu.carry_clear",
                ),
            ),
            instruction(
                cls.Opcode.SEC,
                step(
                    "alu.carry_set",
                ),
            ),
            instruction(
                cls.Opcode.ADC_IMMEDIATE,
                *load_from_pc("alu.lhs.in"),
                step(
                    "a.out",
                    "alu.rhs.in",
                ),
                step(
                    "alu.add",
                ),
                step(
                    "alu.result.out",
                    "a.in",
                ),
            ),
        )

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        data: typing.Optional[typing.Mapping[int, int]] = None,
    ) -> None:
        self.bus = bus.Bus()
        self.__a = register.Register(self.bus, "a")
        self.__instruction_buffer = register.Register(self.bus, "instruction_buffer")
        self.memory = memory.Memory(self.bus, data=data)
        self.__program_counter = program_counter.ProgramCounter(self.bus)
        self.controller = controller.Controller(self.bus, self._controller_entries())
        self.alu = alu.ALU(self.bus)
        super().__init__(
            name or "computer",
            children=frozenset(
                {
                    self.__a,
                    self.__instruction_buffer,
                    self.memory,
                    self.__program_counter,
                    self.controller,
                    self.alu,
                }
            ),
        )

    @property
    def program_counter(self) -> int:
        return self.__program_counter.value

    @program_counter.setter
    def program_counter(self, program_counter: int) -> None:
        self.__program_counter.value = program_counter

    @property
    def a(self) -> int:
        return self.__a.value

    @a.setter
    def a(self, a: int) -> None:
        self.__a.value = a

    @typing.override
    def _str_line(self) -> str:
        return f"Computer(bus={self.bus})"

    @property
    def status(self) -> int:
        return self.alu.status

    @status.setter
    def status(self, status: int) -> None:
        self.alu.status = status

    def update(self) -> None:
        self.controller.apply(self.status)
        super().update()

    def run_instruction(self) -> int:
        return self.controller.run_instruction()

    def run_instructions(self, num: int) -> int:
        return self.controller.run_instructions(num)
