import typing
from pycom import bus, byte, component, controller, memory, program_counter, register


class Computer(component.Component):
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
        self.controller = controller.Controller(self.bus)
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
