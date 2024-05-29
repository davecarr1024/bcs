import dataclasses
import typing
from pycom import errorable

Entry: typing.TypeAlias = typing.Union[
    "reference.Reference",
    "statement.Statement",
]


Value: typing.TypeAlias = typing.Union[
    int,
    "reference.Reference",
]


@dataclasses.dataclass(frozen=True, kw_only=True)
class Program(errorable.Errorable):
    class LabelNotFoundError(errorable.Errorable.Error, KeyError): ...

    @dataclasses.dataclass(frozen=True)
    class Output:
        program: "Program"
        data: dict[int, int] = dataclasses.field(default_factory=dict)

        def with_data(self, data: dict[int, int]) -> "Program.Output":
            return Program.Output(
                self.program,
                self.data | data,
            )

        def with_values_at(self, address: int, *values: int) -> "Program.Output":
            return self.with_data(
                {address + i: value for i, value in enumerate(values)}
            )

        def with_value_at(self, address: int, value: int) -> "Program.Output":
            return self.with_values_at(address, value)

        def as_computer(self) -> "computer.Computer":
            return computer.Computer(data=self.data)

    data: typing.Mapping[int, "reference.Reference"] = dataclasses.field(
        default_factory=dict
    )
    labels: typing.Mapping[str, int] = dataclasses.field(default_factory=dict)
    next_address: int = 0

    def with_(
        self,
        *,
        data: typing.Optional[typing.Mapping[int, "reference.Reference"]] = None,
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

    @classmethod
    def _value(cls, value: Value) -> "reference.Reference":
        match value:
            case int():
                return literal.Literal(value)
            case reference.Reference():
                return value

    def with_value_at(
        self,
        address: int,
        value: Value,
    ) -> "Program":
        return self.with_(data={address: self._value(value)})

    def with_value(self, value: Value) -> "Program":
        value = self._value(value)
        return self.with_value_at(self.next_address, value).at(
            self.next_address + len(value)
        )

    def with_values(self, *values: Value) -> "Program":
        program = self
        for value in values:
            program = program.with_value(value)
        return program

    def with_label_at(self, address: int, name: str) -> "Program":
        return self.with_(labels={name: address})

    def with_label(self, name: str) -> "Program":
        return self.with_label_at(self.next_address, name)

    def with_statement(self, statement: "statement.Statement") -> "Program":
        return statement(self)

    def label(self, name: str) -> int:
        if name not in self.labels:
            raise self.LabelNotFoundError(f"unknown label {name}")
        return self.labels[name]

    def output(self) -> Output:
        output = self.Output(self)
        for address, reference in self.data.items():
            output = reference(output, address)
        return output

    def as_computer(self) -> "computer.Computer":
        return self.output().as_computer()

    def with_entry(self, entry: Entry) -> "Program":
        match entry:
            case reference.Reference():
                return self.with_value(entry)
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
from pycom.computer.references import reference, literal
