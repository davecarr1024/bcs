import dataclasses
import typing
from pycom import bus, byte, component, counter, register


class Controller(component.Component):
    @dataclasses.dataclass(frozen=True)
    class State:
        instruction: int
        instruction_counter: int

    @dataclasses.dataclass(frozen=True)
    class Entry:
        instruction: typing.Optional[int] = None
        instruction_counter: typing.Optional[int] = None
        controls: frozenset[str] = dataclasses.field(default_factory=frozenset)

        def __str__(self) -> str:
            return f"{self.instruction or '*'}.{self.instruction_counter or '*'} {','.join(self.controls)}"

        def matches(self, state: "Controller.State") -> bool:
            return all(
                (
                    self.instruction is None or self.instruction == state.instruction,
                    self.instruction_counter is None
                    or self.instruction_counter == state.instruction_counter,
                )
            )

        @classmethod
        def build(
            cls,
            instruction: typing.Optional[int] = None,
            instruction_counter: typing.Optional[int] = None,
            *controls: str,
        ) -> "Controller.Entry":
            return Controller.Entry(
                instruction,
                instruction_counter,
                frozenset(
                    controls,
                ),
            )

    def __init__(
        self,
        bus: bus.Bus,
        entries: frozenset[Entry],
        name: typing.Optional[str] = None,
    ) -> None:
        self.bus = bus
        self._entries = entries
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
            self.instruction_buffer,
            self.instruction_counter,
        )

    @property
    def entries(self) -> frozenset["Controller.Entry"]:
        return self._entries

    @property
    def entry(self) -> "Controller.Entry":
        state = self.state
        print(f"controller state is {state}")
        entries = [entry for entry in self.entries if entry.matches(state)]
        if len(entries) != 1:
            raise self.Error(
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
