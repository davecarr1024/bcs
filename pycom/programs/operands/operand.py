import abc
import dataclasses
import typing
from pycom.programs import program, statement, references


class Operand(abc.ABC):
    @dataclasses.dataclass(frozen=True, kw_only=True)
    class Statement(statement.Statement):
        opcode: int

        @typing.override
        def __call__(self, program: program.Program) -> program.Program:
            return program.with_value(
                references.Literal(self.opcode),
            )

    @abc.abstractmethod
    def statement(self, opcode: int) -> statement.Statement: ...
