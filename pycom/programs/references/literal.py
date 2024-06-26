import dataclasses
import typing
from pycom.programs import program
from pycom.programs.references import reference


@dataclasses.dataclass(frozen=True)
class Literal(reference.Reference):
    value: int

    @typing.override
    def __call__(
        self,
        output: program.Program.Output,
        address: int,
    ) -> program.Program.Output:
        return output.with_value_at(address, self.value)

    @classmethod
    @typing.override
    def size(cls) -> int:
        return 1
