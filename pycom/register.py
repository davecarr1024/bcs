import dataclasses
import enum
import typing

from pycom import control
from . import byte, bus, component


class Register(component.Component):
    def __init__(
        self,
        bus: bus.Bus,
        name: str,
        on_change: typing.Optional[typing.Callable[[byte.Byte], None]] = None,
    ) -> None:
        self.bus = bus
        self._value = byte.Byte()
        self._on_change = on_change
        self._in = control.Control("in", lambda _: self._communicate())
        self._out = control.Control("out", lambda _: self._communicate())
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

    def __str__(self) -> str:
        return f"Register({self.name}={self.value})"

    @property
    def value(self) -> byte.Byte:
        self._communicate()
        return self._value

    @value.setter
    def value(self, value: byte.Byte) -> None:
        self._value = value
        self._communicate()

    @property
    def in_(self) -> bool:
        return self._in.value

    @in_.setter
    def in_(self, enable_in: bool) -> None:
        self._in.value = enable_in
        self._communicate()

    @property
    def out(self) -> bool:
        return self._out.value

    @out.setter
    def out(self, enable_out: bool) -> None:
        self._out.value = enable_out
        self._communicate()

    @typing.override
    def update(self) -> None:
        self._communicate()
        super().update()

    def _communicate(self) -> None:
        if self.in_:
            self._value = self.bus.value
        elif self.out:
            self.bus.value = self._value
        if self._on_change is not None:
            self._on_change(self._value)
