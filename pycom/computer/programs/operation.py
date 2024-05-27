import dataclasses
import typing
from pycom import byte
from pycom.computer.programs import program, statement


@dataclasses.dataclass(frozen=True, kw_only=True)
class Operation(statement.Statement):
    instruction: "instructions.Instructions"
    operands: typing.Sequence[int | str] = dataclasses.field(default_factory=list)

    def _operands(self, program: program.Program) -> typing.Iterable[int]:
        for operand in self.operands:
            match operand:
                case int():
                    yield operand
                case str():
                    address = program.label(operand)
                    yield address >> byte.Byte.size()
                    yield address % byte.Byte.max()

    @typing.override
    def __call__(self, program: program.Program) -> program.Program:
        return program.with_values(
            self.instruction.value.opcode,
            *self._operands(program),
        )


from pycom.computer.instructions import instructions
