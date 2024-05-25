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
from pycom.computer import instructions


class Computer(component.Component):
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
        self.controller = controller.Controller(
            self.bus, instructions.Instructions.entries()
        )
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
