import dataclasses
import typing
from pycom import byte
from pycom.computer.programs import program
from pycom.computer.references import reference


@dataclasses.dataclass(frozen=True)
class Pair(reference.Reference):
    high: int
    low: int

    @property
    def value(self) -> int:
        return byte.Byte.unpartition(self.high, self.low)

    @classmethod
    def for_value(cls, value: int) -> "Pair":
        high, low, *_ = byte.Byte.partition(value)
        return Pair(high, low)

    @typing.override
    def __call__(
        self,
        output: program.Program.Output,
        address: int,
    ) -> program.Program.Output:
        return output.with_values_at(
            address,
            self.high,
            self.low,
        )

    @classmethod
    @typing.override
    def size(cls) -> int:
        return 2
