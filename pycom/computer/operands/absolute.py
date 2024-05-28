import dataclasses
import typing
from pycom import byte
from pycom.computer.operands import operand
from pycom.computer.programs import program, statement


@dataclasses.dataclass(frozen=True)
class Absolute(operand.Operand):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class Statement(operand.Operand.Statement):
        high_byte: int
        low_byte: int

        @typing.override
        def __call__(self, program: program.Program) -> program.Program:
            return (
                super()
                .__call__(program)
                .with_values(
                    self.high_byte,
                    self.low_byte,
                )
            )

    value: int

    def partition(self) -> tuple[int, int]:
        high, low, *_ = byte.Byte.partition(self.value)
        return high, low

    @staticmethod
    def unpartition(high: int, low: int) -> "Absolute":
        return Absolute(value=byte.Byte.unpartition(high, low))

    @typing.override
    def statement(self, opcode: int) -> statement.Statement:
        high_byte, low_byte = self.partition()
        return self.Statement(
            opcode=opcode,
            high_byte=high_byte,
            low_byte=low_byte,
        )
