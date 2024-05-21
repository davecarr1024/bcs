import collections
import dataclasses
import enum
import typing
from pycom import bus, byte, component, register


class Memory(component.Component):
    class DataMode(enum.Enum):
        IDLE = enum.auto()
        READ_LOW_ADDRESS = enum.auto()
        READ_HIGH_ADDRESS = enum.auto()
        READ_MEMORY = enum.auto()
        WRITE_MEMORY = enum.auto()

    class Action(component.Component.Action["Memory"]): ...

    @dataclasses.dataclass(frozen=True)
    class SetDataMode(Action):
        data_mode: "Memory.DataMode"

        @typing.override
        def __call__(self, component: "Memory") -> None:
            component.data_mode = self.data_mode

    def __init__(
        self,
        bus: bus.Bus,
        name: str | None = None,
        data: typing.Optional[typing.Mapping[int, byte.Byte]] = None,
    ) -> None:
        super().__init__(name)
        self.bus = bus
        self._data: typing.MutableMapping[int, byte.Byte] = collections.defaultdict(
            byte.Byte
        ) | dict(data or {})
        self.low_address_register = register.Register(
            self.bus,
            f"{self.name}_low_address",
        )
        self.high_address_register = register.Register(
            self.bus,
            f"{self.name}_high_address",
        )
        self._data_mode = self.DataMode.IDLE

    @property
    def data(self) -> typing.Mapping[int, byte.Byte]:
        return self._data

    @property
    def low_address(self) -> byte.Byte:
        return self.low_address_register.value

    @low_address.setter
    def low_address(self, low_address: byte.Byte) -> None:
        self.low_address_register.value = low_address

    @property
    def high_address(self) -> byte.Byte:
        return self.high_address_register.value

    @high_address.setter
    def high_address(self, high_address: byte.Byte) -> None:
        self.high_address_register.value = high_address

    @property
    def address(self) -> int:
        return (self.high_address.value << byte.Byte.size()) | self.low_address.value

    @address.setter
    def address(self, address: int) -> None:
        self.low_address.value = address
        self.high_address.value = address >> byte.Byte.size()

    @property
    def _value(self) -> byte.Byte:
        return self._data[self.address]

    @_value.setter
    def _value(self, _value: byte.Byte) -> None:
        self._data[self.address] = _value

    @property
    def value(self) -> byte.Byte:
        self._read_or_write()
        value = self._data[self.address]
        self._read_or_write()
        return value

    @value.setter
    def value(self, value: byte.Byte) -> None:
        self._data[self.address] = value
        self._read_or_write()

    @property
    def data_mode(self) -> DataMode:
        return self._data_mode

    @data_mode.setter
    def data_mode(self, data_mode: DataMode) -> None:
        self._data_mode = data_mode
        self.low_address_register.data_mode = register.Register.DataMode.IDLE
        self.high_address_register.data_mode = register.Register.DataMode.IDLE
        match self._data_mode:
            case self.DataMode.READ_LOW_ADDRESS:
                self.low_address_register.data_mode = register.Register.DataMode.READ
            case self.DataMode.READ_HIGH_ADDRESS:
                self.high_address_register.data_mode = register.Register.DataMode.READ
        self._read_or_write()

    def _read_or_write(self) -> None:
        match self._data_mode:
            case self.DataMode.READ_MEMORY:
                self._read()
            case self.DataMode.WRITE_MEMORY:
                self._write()

    def _read(self) -> None:
        self._value = self.bus.value

    def _write(self) -> None:
        self.bus.value = self._value

    @typing.override
    def tick(self) -> None:
        super().tick()
        self._read_or_write()

    @typing.override
    def apply(self, action: component.Component.Action) -> None:
        match action:
            case Memory.Action():
                action(self)
            case _:
                super().apply(action)
