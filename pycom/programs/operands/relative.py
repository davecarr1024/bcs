import dataclasses
import typing
from pycom.programs import references
from pycom.programs.operands import operand
from pycom.programs import program, statement


@dataclasses.dataclass(frozen=True)
class Relative(operand.Operand):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class Statement(operand.Operand.Statement):
        value: int | str

        @typing.override
        def __call__(self, program: program.Program) -> program.Program:
            program = super().__call__(program)
            match self.value:
                case int():
                    return program.with_value(references.Literal(self.value))
                case str():
                    return program.with_value(references.Relative(self.value))

    value: int | str

    @typing.override
    def statement(self, opcode: int) -> statement.Statement:
        return self.Statement(
            opcode=opcode,
            value=self.value,
        )
