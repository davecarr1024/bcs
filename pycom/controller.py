import dataclasses
import typing
from pycom import bus, byte, component, counter, register


class Controller(component.Component):
    @dataclasses.dataclass(frozen=True)
    class State:
        instruction: byte.Byte
        instruction_counter: byte.Byte

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class Entry:
        instruction: typing.Optional[byte.Byte] = None
        instruction_counter: typing.Optional[byte.Byte] = None
        controls: frozenset[str]

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

    @staticmethod
    def _entry(
        instruction: typing.Optional[int] = None,
        instruction_counter: typing.Optional[int] = None,
        *controls: str,
    ) -> Entry:
        return Controller.Entry(
            instruction=byte.Byte(instruction) if instruction is not None else None,
            instruction_counter=(
                byte.Byte(instruction_counter)
                if instruction_counter is not None
                else None
            ),
            controls=frozenset(controls),
        )

    @staticmethod
    def _preamble() -> frozenset[Entry]:
        return frozenset(
            {
                Controller._entry(
                    None,
                    0,
                    "controller.instruction_counter.increment",
                    "program_counter.high_byte.out",
                    "memory.address_high_byte.in",
                ),
                Controller._entry(
                    None,
                    1,
                    "controller.instruction_counter.increment",
                    "program_counter.low_byte.out",
                    "memory.address_low_byte.in",
                ),
                Controller._entry(
                    None,
                    2,
                    "controller.instruction_counter.increment",
                    "memory.out",
                    "controller.instruction_buffer.in",
                    "program_counter.increment",
                ),
            }
        )

    @staticmethod
    def _instruction(
        instruction: int, *control_sets: typing.Sequence[str]
    ) -> frozenset[Entry]:
        control_sets_: typing.MutableSequence[typing.MutableSequence[str]] = []
        for instruction_counter, control_set in enumerate(control_sets):
            control_set_: typing.MutableSequence[str] = list(control_set)
            if (
                instruction_counter < len(control_sets) - 1
                and "controller.instruction_counter.increment" not in control_set
            ):
                control_set_.append("controller.instruction_counter.increment")
            if (
                instruction_counter == len(control_sets) - 1
                and "controller.instruction_counter.reset" not in control_set
            ):
                control_set_.append("controller.instruction_counter.reset")
            control_sets_.append(control_set_)
            assert (
                "controller.instruction_counter.increment" in control_set_
                or "controller.instruction_counter.reset" in control_set_
            ), str((control_set, control_set_, instruction_counter, len(control_sets)))

        return frozenset(
            {
                Controller._entry(
                    instruction,
                    instruction_counter + len(Controller._preamble()),
                    *controls,
                )
                for instruction_counter, controls in enumerate(control_sets_)
            }
        )

    @staticmethod
    def _default_entries() -> frozenset[Entry]:
        return frozenset.union(
            Controller._preamble(),
            # nop
            Controller._instruction(
                0x00,
                [],
            ),
            # lda immediate
            Controller._instruction(
                0x01,
                [
                    "program_counter.high_byte.out",
                    "memory.address_high_byte.in",
                ],
                [
                    "program_counter.low_byte.out",
                    "memory.address_low_byte.in",
                ],
                [
                    "memory.out",
                    "a.in",
                    "program_counter.increment",
                ],
            ),
            # lda memory
            Controller._instruction(
                0x02,
                [
                    "program_counter.high_byte.out",
                    "memory.address_high_byte.in",
                ],
                [
                    "program_counter.low_byte.out",
                    "memory.address_low_byte.in",
                ],
                [
                    "memory.out",
                    "a.in",
                    "program_counter.increment",
                ],
                [
                    "program_counter.high_byte.out",
                    "memory.address_high_byte.in",
                ],
                [
                    "program_counter.low_byte.out",
                    "memory.address_low_byte.in",
                ],
                [
                    "memory.out",
                    "memory.address_low_byte.in",
                    "program_counter.increment",
                ],
                [
                    "a.out",
                    "memory.address_high_byte.in",
                ],
                [
                    "memory.out",
                    "a.in",
                ],
            ),
        )

    def __init__(
        self,
        bus: bus.Bus,
        *,
        name: typing.Optional[str] = None,
        entries: typing.Optional[frozenset[Entry]] = None,
    ) -> None:
        self.bus = bus
        self._entries = entries or self._default_entries()
        self._instruction_buffer = register.Register(self.bus, "instruction_buffer")
        self._instruction_counter = counter.Counter(self.bus, "instruction_counter")
        super().__init__(
            name or "controller",
            children=frozenset(
                {
                    self._instruction_buffer,
                    self._instruction_counter,
                }
            ),
        )

    @property
    def instruction_buffer(self) -> byte.Byte:
        return self._instruction_buffer.value

    @instruction_buffer.setter
    def instruction_buffer(self, instruction_buffer: byte.Byte) -> None:
        self._instruction_buffer.value = instruction_buffer

    @property
    def instruction_counter(self) -> byte.Byte:
        return self._instruction_counter.value

    @instruction_counter.setter
    def instruction_counter(self, instruction_counter: byte.Byte) -> None:
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
            raise self.Error(f"invalid entries {entries} for state {state}")
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
        while self.instruction_counter.value:
            self.root.update()
            updates += 1
        return updates
