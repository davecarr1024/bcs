import collections
import typing
from pycom.components import bus, byte, component, control, register


class Memory(
    component.Component,
    typing.MutableMapping[int, int],
):
    def __init__(
        self,
        bus: bus.Bus,
        *,
        name: typing.Optional[str] = None,
        data: typing.Optional[typing.Mapping[int, int]] = None,
    ) -> None:
        self.bus = bus
        self._data: typing.MutableMapping[int, byte.Byte] = collections.defaultdict(
            byte.Byte
        )
        if data is not None:
            for address, value in data.items():
                self._data[address] = byte.Byte(value)
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
    def __len__(self) -> int:
        return len(self.data)

    @typing.override
    def __iter__(self) -> typing.Iterator[int]:
        return iter(self.data)

    @typing.override
    def __getitem__(self, address: int) -> int:
        return self.data[address].value

    @typing.override
    def __setitem__(self, address: int, value: int) -> None:
        self._data[address] = byte.Byte(value)

    @typing.override
    def __delitem__(self, address: int) -> None:
        del self._data[address]

    @typing.override
    def _str_line(self) -> str:
        return f"{self.name}({self.address},{byte.Byte.hex_str(self.value)})"

    @property
    def data(self) -> typing.Mapping[int, byte.Byte]:
        return self._data

    @property
    def address_high_byte(self) -> int:
        return self._address_high_byte.value

    @address_high_byte.setter
    def address_high_byte(self, address_high_byte: int) -> None:
        if address_high_byte != self._address_high_byte.value:
            self._address_high_byte.value = address_high_byte
            self._write()

    @property
    def address_low_byte(self) -> int:
        return self._address_low_byte.value

    @address_low_byte.setter
    def address_low_byte(self, address_low_byte: int) -> None:
        if address_low_byte != self._address_low_byte.value:
            self._address_low_byte.value = address_low_byte
            self._write()

    @property
    def _address(self) -> int:
        return byte.Byte.unpartition(
            self.address_high_byte,
            self.address_low_byte,
        )

    @_address.setter
    def _address(self, _address: int) -> None:
        if _address != self._address:
            self.address_high_byte, self.address_low_byte, *_ = byte.Byte.partition(
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
    def _value(self) -> int:
        return self.data[self.address].value

    @_value.setter
    def _value(self, _value: int) -> None:
        self._data[self.address] = byte.Byte(_value)

    @property
    def value(self) -> int:
        self._write()
        value = self._value
        self._write()
        return value

    @value.setter
    def value(self, value: int) -> None:
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
    def tick(self) -> None:
        self._read()
        self._write()
        super().tick()

    def _read(self) -> None:
        if self.in_:
            self._value = self.bus.value

    def _write(self) -> None:
        if self.out:
            self.bus.value = self._value
