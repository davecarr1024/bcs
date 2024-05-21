import dataclasses
import enum
import typing
from pycom import bus, byte, component, register


class ProgramCounter(component.Component):
    class DataMode(enum.Enum):
        IDLE = enum.auto()
        READ_LOW_BYTE = enum.auto()
        READ_HIGH_BYTE = enum.auto()
        WRITE_LOW_BYTE = enum.auto()
        WRITE_HIGH_BYTE = enum.auto()

    class CounterMode(enum.Enum):
        DISABLED = enum.auto()
        ENABLED = enum.auto()
        RESET = enum.auto()

    class Action(component.Component.Action["ProgramCounter"]): ...

    @dataclasses.dataclass(frozen=True)
    class SetDataMode(Action):
        data_mode: "ProgramCounter.DataMode"

        @typing.override
        def __call__(self, component: "ProgramCounter") -> None:
            component.data_mode = self.data_mode

    @dataclasses.dataclass(frozen=True)
    class SetCounterMode(Action):
        counter_mode: "ProgramCounter.CounterMode"

        @typing.override
        def __call__(self, component: "ProgramCounter") -> None:
            component.counter_mode = self.counter_mode

    def __init__(self, bus: bus.Bus, name: str | None = None) -> None:
        super().__init__(name)
        self.bus = bus
        self.low_byte = register.Register(self.bus, f"{self.name}_low_byte")
        self.high_byte = register.Register(self.bus, f"{self.name}_high_byte")
        self._data_mode = self.DataMode.IDLE
        self.counter_mode = self.CounterMode.DISABLED

    @property
    def data_mode(self) -> DataMode:
        return self._data_mode

    @data_mode.setter
    def data_mode(self, data_mode: DataMode) -> None:
        self._data_mode = data_mode
        match self._data_mode:
            case self.DataMode.READ_LOW_BYTE:
                self.low_byte.data_mode = register.Register.DataMode.READ
                self.high_byte.data_mode = register.Register.DataMode.IDLE
            case self.DataMode.READ_HIGH_BYTE:
                self.low_byte.data_mode = register.Register.DataMode.IDLE
                self.high_byte.data_mode = register.Register.DataMode.READ
            case self.DataMode.WRITE_LOW_BYTE:
                self.low_byte.data_mode = register.Register.DataMode.WRITE
                self.high_byte.data_mode = register.Register.DataMode.IDLE
            case self.DataMode.WRITE_HIGH_BYTE:
                self.low_byte.data_mode = register.Register.DataMode.IDLE
                self.high_byte.data_mode = register.Register.DataMode.WRITE

    @property
    def low_value(self) -> byte.Byte:
        return self.low_byte.value

    @low_value.setter
    def low_value(self, low_value: byte.Byte) -> None:
        self.low_byte.value = low_value

    @property
    def high_value(self) -> byte.Byte:
        return self.high_byte.value

    @high_value.setter
    def high_value(self, high_value: byte.Byte) -> None:
        self.high_byte.value = high_value

    @property
    def value(self) -> int:
        return (self.high_value.value << byte.Byte.size()) | self.low_value.value

    @value.setter
    def value(self, value: int) -> None:
        self.low_value.value = value
        self.high_value.value = value >> byte.Byte.size()

    @typing.override
    def tick(self) -> None:
        match self.counter_mode:
            case self.CounterMode.ENABLED:
                self.value += 1
            case self.CounterMode.RESET:
                self.value = 0
        self.low_byte.tick()
        self.high_byte.tick()
        super().tick()

    @typing.override
    def apply(self, action: component.Component.Action) -> None:
        match action:
            case ProgramCounter.Action():
                action(self)
            case _:
                super().apply(action)
