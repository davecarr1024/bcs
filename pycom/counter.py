import dataclasses
import enum
import typing
from . import byte, bus, component, register


class Counter(register.Register):
    class CounterMode(enum.Enum):
        DISABLED = enum.auto()
        ENABLED = enum.auto()
        RESET = enum.auto()

    class Action(component.Component.Action["Counter"]): ...

    @dataclasses.dataclass(frozen=True)
    class SetCounterMode(Action):
        counter_mode: "Counter.CounterMode"

        @typing.override
        def __call__(self, counter: "Counter") -> None:
            counter.counter_mode = self.counter_mode

    def __init__(
        self,
        bus: bus.Bus,
        name: str,
    ) -> None:
        super().__init__(bus, name)
        self.counter_mode = self.CounterMode.DISABLED

    @typing.override
    def update(self) -> None:
        match self.counter_mode:
            case self.CounterMode.DISABLED:
                ...
            case self.CounterMode.ENABLED:
                self.value = byte.Byte(self.value.value + 1)
            case self.CounterMode.RESET:
                self.value = byte.Byte(0)
        super().update()

    @typing.override
    def apply(self, action: component.Component.Action) -> None:
        match action:
            case Counter.Action():
                action(self)
            case _:
                super().apply(action)
