import dataclasses
import typing
from pycom import byte
from pycom.computer.programs import program
from pycom.computer.references import reference


@dataclasses.dataclass(frozen=True)
class Absolute(reference.Reference):
    value: str

    @typing.override
    def __call__(
        self,
        output: program.Program.Output,
        address: int,
    ) -> program.Program.Output:
        high, low, *_ = byte.Byte.partition(output.program.label(self.value))
        return output.with_values_at(address, high, low)

    @typing.override
    def __len__(self) -> int:
        return 2
