import collections
import typing
from pycom import bus, byte, component, control, register


class Memory(component.Component):
    def __init__(
        self,
        bus: bus.Bus,
        name: typing.Optional[str] = None,
        data: typing.Optional[typing.Mapping[int, byte.Byte]] = None,
    ) -> None:
        self.bus = bus
        self._data: typing.MutableMapping[int, byte.Byte] = collections.defaultdict(
            byte.Byte
        ) | dict(data or {})
        self._in = control.Control("in", lambda _: self._communicate())
        self._out = control.Control("out", lambda _: self._communicate())
        self._address_high_byte = register.Register(
            self.bus,
            "address_high_byte",
            lambda _: self._communicate(),
        )
        self._address_low_byte = register.Register(
            self.bus,
            "address_low_byte",
            lambda _: self._communicate(),
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

    @property
    def data(self) -> typing.Mapping[int, byte.Byte]:
        return self._data

    @property
    def address_high_byte(self) -> byte.Byte:
        return self._address_high_byte.value

    @address_high_byte.setter
    def address_high_byte(self, address_high_byte: byte.Byte) -> None:
        self._address_high_byte.value = address_high_byte
        self._communicate()

    @property
    def address_low_byte(self) -> byte.Byte:
        return self._address_low_byte.value

    @address_low_byte.setter
    def address_low_byte(self, address_low_byte: byte.Byte) -> None:
        self._address_low_byte.value = address_low_byte
        self._communicate()

    @property
    def address(self) -> int:
        return byte.Byte.bytes_to_int(self.address_high_byte, self.address_low_byte)

    @address.setter
    def address(self, address: int) -> None:
        self.address_high_byte, self.address_low_byte, *_ = byte.Byte.int_to_bytes(
            address
        )
        self._communicate()

    @property
    def value(self) -> byte.Byte:
        self._communicate()
        value = self.data[self.address]
        self._communicate()
        return value

    @value.setter
    def value(self, value: byte.Byte) -> None:
        self._data[self.address] = value
        self._communicate()

    def _communicate(self) -> None:
        ...
