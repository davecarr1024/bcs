import dataclasses
import typing
from pycom import byte
from pycom.computer import references
from pycom.computer.operands import operand
from pycom.computer.programs import program, statement


@dataclasses.dataclass(frozen=True)
class Absolute(operand.Operand):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class Statement(operand.Operand.Statement):
        value: int | str

        @typing.override
        def __call__(self, program: program.Program) -> program.Program:
            program = super().__call__(program)
            match self.value:
                case int():
                    high, low = byte.Byte.partition(self.value)
                    return program.with_value(references.Pair.for_value(self.value))
                case str():
                    return program.with_value(references.Absolute(self.value))

    value: int | str

    @typing.override
    def statement(self, opcode: int) -> statement.Statement:
        return self.Statement(
            opcode=opcode,
            value=self.value,
        )
