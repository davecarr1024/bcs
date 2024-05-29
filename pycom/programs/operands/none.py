import typing
from pycom.programs.operands import operand
from pycom.programs import statement


class None_(operand.Operand):
    class Statement(operand.Operand.Statement): ...

    @typing.override
    def statement(self, opcode: int) -> statement.Statement:
        return self.Statement(opcode=opcode)
