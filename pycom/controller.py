import dataclasses
import typing
from pycom import bus, component, counter, errorable, register, signal


class Controller(component.Component):
    class EntryError(errorable.Errorable.Error, KeyError): ...

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class SignalValue:
        name: str
        value: bool

        @staticmethod
        def for_signal(signal: signal.Signal) -> "Controller.SignalValue":
            return Controller.SignalValue(
                name=signal.name,
                value=signal.value,
            )

        @staticmethod
        def for_component(
            component: component.Component,
        ) -> frozenset["Controller.SignalValue"]:
            return frozenset(
                {
                    Controller.SignalValue.for_signal(signal)
                    for signal in component.all_signals
                }
            )

    @dataclasses.dataclass(frozen=True)
    class SignalValueMap(errorable.Errorable, typing.Mapping[str, bool]):
        class SignalNotFoundError(errorable.Errorable, KeyError): ...

        _values: frozenset["Controller.SignalValue"] = dataclasses.field(
            default_factory=frozenset
        )

        @staticmethod
        def for_component(
            component: component.Component,
        ) -> "Controller.SignalValueMap":
            return Controller.SignalValueMap(
                frozenset(
                    {
                        Controller.SignalValue.for_signal(signal)
                        for signal in component.all_signals
                    }
                )
            )

        @staticmethod
        def build(**values: bool) -> "Controller.SignalValueMap":
            return Controller.SignalValueMap(
                frozenset(
                    {
                        Controller.SignalValue(
                            name=name,
                            value=value,
                        )
                        for name, value in values.items()
                    }
                )
            )

        @property
        def values_by_name(self) -> typing.Mapping[str, bool]:
            return {value.name: value.value for value in self._values}

        @typing.override
        def __len__(self) -> int:
            return len(self.values_by_name)

        @typing.override
        def __getitem__(self, name: str) -> bool:
            try:
                return self.values_by_name[name]
            except KeyError as e:
                raise self.SignalNotFoundError(f"failed to get signal {name}: {e}")

        @typing.override
        def __iter__(self) -> typing.Iterator[str]:
            return iter(self.values_by_name)

        def matches(self, rhs: "Controller.SignalValueMap") -> bool:
            for name, value in self.items():
                if name not in rhs or value != rhs[name]:
                    return False
            return True

    @dataclasses.dataclass(
        frozen=True,
        kw_only=True,
    )
    class State:
        instruction: int
        instruction_counter: int
        signals: "Controller.SignalValueMap" = dataclasses.field(
            default_factory=lambda: Controller.SignalValueMap()
        )

    @dataclasses.dataclass(
        frozen=True,
        kw_only=True,
    )
    class Entry:
        instruction: typing.Optional[int] = None
        instruction_counter: typing.Optional[int] = None
        signals: typing.Optional["Controller.SignalValueMap"] = None
        controls: frozenset[str] = dataclasses.field(default_factory=frozenset)

        def __str__(self) -> str:
            return f"{self.instruction or '*'}.{self.instruction_counter or '*'} {','.join(self.controls)}"

        def matches(self, state: "Controller.State") -> bool:
            return all(
                (
                    self.instruction is None or self.instruction == state.instruction,
                    self.instruction_counter is None
                    or self.instruction_counter == state.instruction_counter,
                    self.signals is None or self.signals.matches(state.signals),
                )
            )

    def __init__(
        self,
        bus: bus.Bus,
        entries: typing.Iterable[Entry],
        name: typing.Optional[str] = None,
    ) -> None:
        self.bus = bus
        self._entries = frozenset(entries)
        self._instruction_buffer = register.Register(self.bus, "instruction_buffer")
        self._instruction_counter = counter.Counter(self.bus, "instruction_counter")
        self._address_buffer = register.Register(self.bus, "address_buffer")
        super().__init__(
            name or "controller",
            children=frozenset(
                {
                    self._instruction_buffer,
                    self._instruction_counter,
                    self._address_buffer,
                }
            ),
        )

    @property
    def instruction_buffer(self) -> int:
        return self._instruction_buffer.value

    @instruction_buffer.setter
    def instruction_buffer(self, instruction_buffer: int) -> None:
        self._instruction_buffer.value = instruction_buffer

    @property
    def instruction_counter(self) -> int:
        return self._instruction_counter.value

    @instruction_counter.setter
    def instruction_counter(self, instruction_counter: int) -> None:
        self._instruction_counter.value = instruction_counter

    @property
    def state(self) -> State:
        return self.State(
            instruction=self.instruction_buffer,
            instruction_counter=self.instruction_counter,
            signals=self.SignalValueMap.for_component(self.root),
        )

    @property
    def entries(self) -> frozenset["Controller.Entry"]:
        return self._entries

    @property
    def entry(self) -> "Controller.Entry":
        state = self.state
        print(f"controller state is {state}")
        entries = [entry for entry in self.entries if entry.matches(state)]
        print(f"matched entries {entries}")
        if len(entries) != 1:
            raise self.EntryError(
                f"invalid entries {entries} for state {state}: entries are {'\n'.join(map(str, self.entries))}"
            )
        return entries[0]

    def apply(self) -> None:
        entry = self.entry
        print(f"running entry {entry}\nwith root {self.root}\n")
        try:
            self.root.set_controls(*entry.controls)
        except self.Error as e:
            raise self.Error(
                f"failed to apply entry {entry} with state {self.state}: {e}"
            )

    def run_instruction(self) -> int:
        self.root.update()
        updates = 1
        while self.instruction_counter:
            self.root.update()
            updates += 1
        return updates

    def run_instructions(self, num: int) -> int:
        return sum(self.run_instruction() for _ in range(num))

    @typing.override
    def validate(self) -> None:
        entry_signals: frozenset[str] = frozenset().union(
            *[
                frozenset(entry.signals.keys())
                for entry in self.entries
                if entry.signals is not None
            ],
        )
        root_signals: frozenset[str] = frozenset(self.root.signals_by_name.keys())
        if not entry_signals.issubset(root_signals):
            raise self.ValidationError(
                f"controller entries have unknown signals {entry_signals-root_signals}"
            )
        super().validate()
