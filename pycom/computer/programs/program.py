import dataclasses
import typing
from pycom import errorable

Entry: typing.TypeAlias = typing.Union[
    int,
    str,
    "instructions.Instructions",
    "statement.Statement",
]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Program(errorable.Errorable):
    class LabelNotFoundError(errorable.Errorable.Error, KeyError): ...

    data: typing.Mapping[int, int] = dataclasses.field(default_factory=dict)
    labels: typing.Mapping[str, int] = dataclasses.field(default_factory=dict)
    next_address: int = 0

    def with_(
        self,
        *,
        data: typing.Optional[typing.Mapping[int, int]] = None,
        labels: typing.Optional[typing.Mapping[str, int]] = None,
        next_address: typing.Optional[int] = 0,
    ) -> "Program":
        return Program(
            data=dict(self.data) | (dict(data or {})),
            labels=dict(self.labels) | (dict(labels or {})),
            next_address=(
                next_address if next_address is not None else self.next_address
            ),
        )

    def at(self, next_address: int) -> "Program":
        return self.with_(next_address=next_address)

    def with_value_at(
        self,
        address: int,
        value: int,
    ) -> "Program":
        return self.with_(data={address: value})

    def with_value(self, value: int) -> "Program":
        return self.with_(
            data={self.next_address: value},
            next_address=self.next_address + 1,
        )

    def with_values(self, *values: int) -> "Program":
        return self.with_(
            data={self.next_address + i: value for i, value in enumerate(values)},
            next_address=self.next_address + len(values),
        )

    def with_label(self, name: str) -> "Program":
        return self.with_(labels={name: self.next_address})

    def with_statement(self, statemewnt: "statement.Statement") -> "Program":
        return statemewnt(self)

    def label(self, name: str) -> int:
        if name not in self.labels:
            raise self.LabelNotFoundError(f"unknown label {name}")
        return self.labels[name]

    def as_computer(self) -> "computer.Computer":
        return computer.Computer(data=self.data)

    def with_entry(self, entry: Entry) -> "Program":
        match entry:
            case int():
                return self.with_value(entry)
            case str():
                return self.with_label(entry)
            case instructions.Instructions():
                return self.with_value(entry.value.opcode)
            case statement.Statement():
                return self.with_statement(entry)

    def with_entries(
        self,
        *entries: Entry,
    ) -> "Program":
        program = self
        for entry in entries:
            program = program.with_entry(entry)
        return program

    @classmethod
    def build(
        cls,
        *entries: Entry,
    ) -> "Program":
        return Program().with_entries(*entries)


from . import statement
from pycom.computer import computer
from pycom.computer.instructions import instructions
