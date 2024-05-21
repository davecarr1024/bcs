import typing
from pycom import bus, byte, control, register


class Counter(register.Register):
    def __init__(
        self,
        bus: bus.Bus,
        name: str,
        on_change: typing.Optional[typing.Callable[[byte.Byte], None]] = None,
    ) -> None:
        super().__init__(bus, name, on_change)
        self._increment = control.Control(
            "increment",
            component=self,
        )
        self._reset = control.Control(
            "reset",
            component=self,
        )

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
    def update(self) -> None:
        if self.increment:
            self.value = byte.Byte(self.value.value + 1)
        elif self.reset:
            self.value = byte.Byte()
        super().update()
