import typing
from pycom.components import bus, byte, control, register


class Counter(register.Register):
    def __init__(
        self,
        bus: bus.Bus,
        name: str,
        on_change: typing.Optional[typing.Callable[[byte.Byte], None]] = None,
        value: int = 0,
    ) -> None:
        super().__init__(
            bus,
            name,
            on_change,
            value,
        )
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
    def tick(self) -> None:
        if self.increment:
            self.value += 1
        elif self.reset:
            self.value = 0
        super().tick()
