import dataclasses
import typing
from pycom.components import bus, byte, component, counter, errorable, register


class Controller(component.Component):
    class EntryError(errorable.Errorable.Error, KeyError): ...

    @dataclasses.dataclass(
        frozen=True,
        kw_only=True,
    )
    class State:
        instruction: int
        instruction_counter: int
        status: int

    @dataclasses.dataclass(
        frozen=True,
        kw_only=True,
    )
    class Entry:
        instruction: typing.Optional[int] = None
        instruction_counter: typing.Optional[int] = None
        status_mask: int = 0
        status_value: int = 0
        controls: frozenset[str] = dataclasses.field(default_factory=frozenset)

        def __str__(self) -> str:
            def _str(value: int | None) -> str:
                return byte.Byte.hex_str(value) if value is not None else "*"

            return f"{_str(self.instruction)}.{_str(self.instruction_counter)} {','.join(self.controls)}"

        def matches(self, state: "Controller.State") -> bool:
            return all(
                (
                    self.instruction is None or self.instruction == state.instruction,
                    self.instruction_counter is None
                    or self.instruction_counter == state.instruction_counter,
                    state.status & self.status_mask == self.status_value,
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

    def state(self, status: int) -> State:
        return self.State(
            instruction=self.instruction_buffer,
            instruction_counter=self.instruction_counter,
            status=status,
        )

    @property
    def entries(self) -> frozenset["Controller.Entry"]:
        return self._entries

    def entry(self, status: int) -> "Controller.Entry":
        state = self.state(status)
        print(f"controller state is {state}")
        entries = [entry for entry in self.entries if entry.matches(state)]
        print(f"matched entries {entries}")
        if len(entries) != 1:
            raise self.EntryError(
                f"invalid entries {entries} for state {state}: entries are {'\n'.join(map(str, self.entries))}"
            )
        return entries[0]

    def apply(self, status: int) -> None:
        entry = self.entry(status)
        print(f"running entry {entry}\nwith root {self.root}\n")
        try:
            self.root.set_controls(*entry.controls)
        except self.Error as e:
            raise self.Error(
                f"failed to apply entry {entry} with state {self.state}: {e}"
            )

    def run_instruction(self) -> int:
        self.root.tick()
        updates = 1
        while self.instruction_counter:
            self.root.tick()
            updates += 1
        return updates

    def run_instructions(self, num: int) -> int:
        return sum(self.run_instruction() for _ in range(num))
