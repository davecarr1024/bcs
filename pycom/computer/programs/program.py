import dataclasses
import typing
from pycom import byte, errorable

Entry: typing.TypeAlias = typing.Union[
    int,
    str,
    "instructions.Instructions",
    "statement.Statement",
]

Value: typing.TypeAlias = typing.Union[
    int,
    str,
]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Program(errorable.Errorable):
    class LabelNotFoundError(errorable.Errorable.Error, KeyError): ...

    data: typing.Mapping[int, Value] = dataclasses.field(default_factory=dict)
    labels: typing.Mapping[str, int] = dataclasses.field(default_factory=dict)
    next_address: int = 0

    def with_(
        self,
        *,
        data: typing.Optional[typing.Mapping[int, Value]] = None,
        labels: typing.Optional[typing.Mapping[str, int]] = None,
        next_address: typing.Optional[int] = None,
    ) -> "Program":
        return Program(
            data=dict(self.data) | (dict(data or {})),
            labels=dict(self.labels) | (dict(labels or {})),
            next_address=(
                next_address if next_address is not None else self.next_address
            ),
        )

    def at(self, next_address: int | str) -> "Program":
        match next_address:
            case int():
                return self.with_(next_address=next_address)
            case str():
                return self.with_(next_address=self.label(next_address))

    def _offset_for_value(self, value: Value) -> int:
        match value:
            case int():
                return 1
            case str():
                return 2

    def with_value_at(
        self,
        address: int,
        value: int,
    ) -> "Program":
        return self.with_(data={address: value})

    def with_value(self, value: Value) -> "Program":
        return self.with_(
            data={self.next_address: value},
            next_address=self.next_address + self._offset_for_value(value),
        )

    def with_values(self, *values: Value) -> "Program":
        data: typing.MutableMapping[int, Value] = {}
        offset = 0
        for value in values:
            data[self.next_address + offset] = value
            offset += self._offset_for_value(value)
        return self.with_(
            data=data,
            next_address=self.next_address + offset,
        )

    def with_label_at(self, name: str, address: int) -> "Program":
        return self.with_(labels={name: address})

    def with_label(self, name: str) -> "Program":
        return self.with_label_at(name, self.next_address)

    def with_statement(self, statemewnt: "statement.Statement") -> "Program":
        return statemewnt(self)

    def label(self, name: str) -> int:
        if name not in self.labels:
            raise self.LabelNotFoundError(f"unknown label {name}")
        return self.labels[name]

    def finalize_data(self) -> typing.Mapping[int, int]:
        data: typing.MutableMapping[int, int] = {}
        for address, value in self.data.items():
            match value:
                case int():
                    data[address] = value
                case str():
                    value = self.label(value)
                    data[address] = value >> byte.Byte.size()
                    data[address + 1] = value % byte.Byte.max()
        return data

    def as_computer(self) -> "computer.Computer":
        return computer.Computer(data=self.finalize_data())

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

    @classmethod
    def computer(cls, *entries: Entry) -> "computer.Computer":
        return cls.build(*entries).as_computer()


from . import statement
from pycom.computer import computer
from pycom.computer.instructions import instructions
