import typing
from pycom.components import (
    alu,
    bus,
    clock,
    component,
    controller,
    memory,
    program_counter,
    register,
)
from pycom.instructions import instructions
from pycom.programs import program


class Computer(component.Component):
    STACK_POINTER_ADDR = 0x00FE
    STACK_ADDR = 0x0100

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        data: typing.Optional[typing.Mapping[int, int]] = None,
    ) -> None:
        self.bus = bus.Bus()
        self.__a = register.Register(self.bus, "a")
        self.__x = register.Register(self.bus, "x")
        self.__y = register.Register(self.bus, "y")
        self.__instruction_buffer = register.Register(self.bus, "instruction_buffer")
        self.memory = memory.Memory(self.bus, data=data)
        self.__program_counter = program_counter.ProgramCounter(self.bus)
        self.controller = controller.Controller(
            self.bus, instructions.Instructions.entries()
        )
        self.clock = clock.Clock()
        self.alu = alu.ALU(self.bus)
        super().__init__(
            name or "computer",
            children=frozenset(
                {
                    self.__a,
                    self.__x,
                    self.__y,
                    self.__instruction_buffer,
                    self.memory,
                    self.__program_counter,
                    self.controller,
                    self.alu,
                    self.clock,
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

    @property
    def x(self) -> int:
        return self.__x.value

    @x.setter
    def x(self, x: int) -> None:
        self.__x.value = x

    @property
    def y(self) -> int:
        return self.__y.value

    @y.setter
    def y(self, y: int) -> None:
        self.__y.value = y

    @typing.override
    def _str_line(self) -> str:
        return f"Computer(bus={self.bus})"

    @property
    def status(self) -> int:
        return self.alu.status

    @status.setter
    def status(self, status: int) -> None:
        self.alu.status = status

    def tick(self) -> None:
        self.controller.apply(self.status)
        super().tick()

    def run_instruction(self) -> int:
        return self.controller.run_instruction()

    def run_instructions(self, num: int) -> int:
        return self.controller.run_instructions(num)

    def run(self) -> int:
        return self.clock.run()

    @classmethod
    def build(cls, *entries: program.Entry) -> "Computer":
        return cls.for_program(program.Program.build(*entries))

    @classmethod
    def for_program(cls, program: program.Program) -> "Computer":
        return program.as_computer()
