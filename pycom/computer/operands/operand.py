import abc
import dataclasses
import typing
from pycom.computer import references
from pycom.computer.programs import program, statement


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
