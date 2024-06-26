import typing
from pycom.components import bus, byte, component, control, register


class ProgramCounter(component.Component):
    def __init__(
        self,
        bus: bus.Bus,
        name: str | None = None,
    ) -> None:
        self.bus = bus
        self._increment = control.Control("increment")
        self._reset = control.Control("reset")
        self._low_byte = register.Register(self.bus, "low_byte")
        self._high_byte = register.Register(self.bus, "high_byte")
        super().__init__(
            name or "program_counter",
            children=frozenset({self._low_byte, self._high_byte}),
            controls=frozenset({self._increment, self._reset}),
        )

    @typing.override
    def _str_line(self) -> str:
        return f"{self.name}({byte.Byte.hex_str(self.value)})"

    @property
    def low_byte(self) -> int:
        return self._low_byte.value

    @low_byte.setter
    def low_byte(self, low: int) -> None:
        self._low_byte.value = low

    @property
    def high_byte(self) -> int:
        return self._high_byte.value

    @high_byte.setter
    def high_byte(self, high: int) -> None:
        self._high_byte.value = high

    @property
    def value(self) -> int:
        return byte.Byte.unpartition(self.high_byte, self.low_byte)

    @value.setter
    def value(self, value: int) -> None:
        self.high_byte, self.low_byte, *_ = byte.Byte.partition(value)

    @property
    def increment(self) -> bool:
        return self._increment.value

    @increment.setter
    def increment(self, increment: bool) -> None:
        self._increment.value = increment

    @property
    def reset(self) -> bool:
        return self._reset.value

    @reset.setter
    def reset(self, reset: bool) -> None:
        self._reset.value = reset

    @typing.override
    def tick(self) -> None:
        if self.increment:
            self.value += 1
        elif self.reset:
            self.value = 0
        super().tick()
