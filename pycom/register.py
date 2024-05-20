import dataclasses
import enum
import typing
from . import byte, bus, component


class Register(component.Component):
    class DataMode(enum.Enum):
        IDLE = enum.auto()
        READ = enum.auto()
        WRITE = enum.auto()

    class Action(component.Component.Action["Register"]):
        ...

    @dataclasses.dataclass(frozen=True)
    class SetDataMode(Action):
        data_mode: "Register.DataMode"

        @typing.override
        def __call__(self, register: "Register") -> None:
            register.data_mode = self.data_mode

    def __init__(
        self,
        bus: bus.Bus,
        name: str,
    ) -> None:
        component.Component.__init__(self, name)
        self.bus = bus
        self._value = byte.Byte()
        self._data_mode = self.DataMode.IDLE

    def __str__(self) -> str:
        return f"Register({self.name}={self.value})"

    @property
    def value(self) -> byte.Byte:
        self._read_or_write()
        return self._value

    @value.setter
    def value(self, value: byte.Byte) -> None:
        self._value = value
        self._read_or_write()

    @property
    def data_mode(self) -> DataMode:
        return self._data_mode

    @data_mode.setter
    def data_mode(self, data_mode: DataMode) -> None:
        self._data_mode = data_mode
        self._read_or_write()

    @typing.override
    def update(self) -> None:
        self._read_or_write()
        super().update()

    def _read_or_write(self) -> None:
        match self.data_mode:
            case self.DataMode.READ:
                self._read()
            case self.DataMode.WRITE:
                self._write()

    @typing.override
    def apply(self, action: component.Component.Action) -> None:
        match action:
            case Register.Action():
                action(self)
            case _:
                super().apply(action)

    def _read(self) -> None:
        self._value = self.bus.value

    def _write(self) -> None:
        self.bus.value = self._value
