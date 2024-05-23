import collections
import typing
from pycom import bus, byte, component, control, register


class Memory(component.Component):
    def __init__(
        self,
        bus: bus.Bus,
        *,
        name: typing.Optional[str] = None,
        data: typing.Optional[typing.Mapping[int, byte.Byte]] = None,
    ) -> None:
        self.bus = bus
        self._data: typing.MutableMapping[int, byte.Byte] = collections.defaultdict(
            byte.Byte
        ) | dict(data or {})
        self._in = control.Control("in", lambda _: self._write())
        self._out = control.Control("out", lambda _: self._write())
        self._address_high_byte = register.Register(
            self.bus,
            "address_high_byte",
            lambda _: self._write(),
        )
        self._address_low_byte = register.Register(
            self.bus,
            "address_low_byte",
            lambda _: self._write(),
        )
        super().__init__(
            name or "memory",
            children=frozenset(
                {
                    self._address_high_byte,
                    self._address_low_byte,
                }
            ),
            controls=frozenset(
                {
                    self._in,
                    self._out,
                }
            ),
        )

    @typing.override
    def _str_line(self) -> str:
        return f"{self.name}({self.address},{self.value})"

    @property
    def data(self) -> typing.Mapping[int, byte.Byte]:
        return self._data

    @property
    def address_high_byte(self) -> byte.Byte:
        return self._address_high_byte.value

    @address_high_byte.setter
    def address_high_byte(self, address_high_byte: byte.Byte) -> None:
        if address_high_byte != self._address_high_byte.value:
            self._address_high_byte.value = address_high_byte
            self._write()

    @property
    def address_low_byte(self) -> byte.Byte:
        return self._address_low_byte.value

    @address_low_byte.setter
    def address_low_byte(self, address_low_byte: byte.Byte) -> None:
        if address_low_byte != self._address_low_byte.value:
            self._address_low_byte.value = address_low_byte
            self._write()

    @property
    def _address(self) -> int:
        return byte.Byte.bytes_to_int(self.address_high_byte, self.address_low_byte)

    @_address.setter
    def _address(self, _address: int) -> None:
        if _address != self._address:
            self.address_high_byte, self.address_low_byte, *_ = byte.Byte.int_to_bytes(
                _address
            )

    @property
    def address(self) -> int:
        return self._address

    @address.setter
    def address(self, address: int) -> None:
        if address != self.address:
            self._address = address
            self._write()

    @property
    def _value(self) -> byte.Byte:
        return self.data[self.address]

    @_value.setter
    def _value(self, _value: byte.Byte) -> None:
        self._data[self.address] = _value

    @property
    def value(self) -> byte.Byte:
        self._write()
        value = self._value
        self._write()
        return value

    @value.setter
    def value(self, value: byte.Byte) -> None:
        if value != self._value:
            self._value = value
            self._write()

    @property
    def in_(self) -> bool:
        return self._in.value

    @in_.setter
    def in_(self, in_: bool) -> None:
        self._in.value = in_
        self._write()

    @property
    def out(self) -> bool:
        return self._out.value

    @out.setter
    def out(self, out: bool) -> None:
        self._out.value = out
        self._write()

    @typing.override
    def update(self) -> None:
        self._read()
        self._write()
        super().update()

    def _read(self) -> None:
        if self.in_:
            self._value = self.bus.value

    def _write(self) -> None:
        if self.out:
            self.bus.value = self._value
