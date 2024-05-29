import dataclasses
import typing
from pycom import byte, errorable
from pycom.computer.programs import program
from pycom.computer.references import reference


@dataclasses.dataclass(frozen=True)
class Relative(reference.Reference, errorable.Errorable):
    value: str

    @typing.override
    def __call__(
        self,
        output: program.Program.Output,
        address: int,
    ) -> program.Program.Output:
        value_address = output.program.label(self.value)
        value_high_byte, value_low_byte, *_ = byte.Byte.partition(value_address)
        address_high_byte, *_ = byte.Byte.partition(address)
        if value_high_byte != address_high_byte:
            raise self.Error(
                f"relative reference {self} at {byte.Byte.hex_str(value_address)} referred to from distant address {byte.Byte.hex_str(address)}"
            )
        return output.with_value_at(address, value_low_byte)

    @typing.override
    def __len__(self) -> int:
        return 1
