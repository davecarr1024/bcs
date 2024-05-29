import typing
from pycom.computer.operands import operand
from pycom.computer.programs import statement


class None_(operand.Operand):
    class Statement(operand.Operand.Statement): ...

    @typing.override
    def statement(self, opcode: int) -> statement.Statement:
        return self.Statement(opcode=opcode)
