import typing
from pycom import byte, bus, component, control


class Register(component.Component):
    def __init__(
        self,
        bus: bus.Bus,
        name: str,
        on_change: typing.Optional[typing.Callable[[byte.Byte], None]] = None,
        value: int = 0,
    ) -> None:
        self.bus = bus
        self.__value = byte.Byte(value)
        self._on_change = on_change
        self._in = control.Control("in", lambda _: self._write())
        self._out = control.Control("out", lambda _: self._write())
        component.Component.__init__(
            self,
            name,
            controls=frozenset(
                {
                    self._in,
                    self._out,
                }
            ),
        )

    @typing.override
    def _str_line(self) -> str:
        return f"{self.name}={self.value}"

    @property
    def value(self) -> int:
        self._write()
        return self.__value.value

    @value.setter
    def value(self, value: int) -> None:
        self.__value = byte.Byte(value)
        self._write()

    @property
    def in_(self) -> bool:
        return self._in.value

    @in_.setter
    def in_(self, enable_in: bool) -> None:
        self._in.value = enable_in
        self._write()

    @property
    def out(self) -> bool:
        return self._out.value

    @out.setter
    def out(self, enable_out: bool) -> None:
        self._out.value = enable_out
        self._write()

    @typing.override
    def update(self) -> None:
        self._read()
        self._write()
        super().update()

    def _read(self) -> None:
        if self.in_:
            old_value = self.__value
            self.__value = byte.Byte(self.bus.value)
            if old_value != self.__value and self._on_change is not None:
                self._on_change(self.__value)

    def _write(self) -> None:
        if self.out:
            self.bus.value = self.__value.value
