import dataclasses
import typing
from pycom.computer.operands import operand
from pycom.computer.programs import program, statement


@dataclasses.dataclass(frozen=True)
class Immediate(operand.Operand):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class Statement(operand.Operand.Statement):
        value: int

        @typing.override
        def __call__(self, program: program.Program) -> program.Program:
            return super().__call__(program).with_value(self.value)

    value: int

    @typing.override
    def statement(self, opcode: int) -> statement.Statement:
        return self.Statement(
            opcode=opcode,
            value=self.value,
        )
