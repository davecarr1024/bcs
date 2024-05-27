import dataclasses
import typing
from pycom import byte
from pycom.computer.programs import program, statement


@dataclasses.dataclass(frozen=True, kw_only=True)
class Operation(statement.Statement):
    instruction: "instructions.Instructions"
    operands: typing.Sequence[program.Value] = dataclasses.field(default_factory=list)

    @typing.override
    def __call__(self, program: program.Program) -> program.Program:
        return program.with_values(
            self.instruction.value.opcode,
            *self.operands,
        )


from pycom.computer.instructions import instructions
