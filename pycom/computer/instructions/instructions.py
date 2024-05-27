import enum
import typing
from pycom import controller
from pycom.computer.instructions import instruction
from pycom.computer.instructions import instruction


class Instructions(enum.Enum):
    NOP = instruction.Instruction.build(
        0xEA,
    )
    LDA_IMMEDIATE = instruction.Instruction.build(
        0xA9,
        *instruction.Instruction.load_from_pc("a.in"),
    )
    LDA_ABSOLUTE = instruction.Instruction.build(
        0xAD,
        *instruction.Instruction.load_from_addr_at_pc("a.in"),
    )
    STA_ABSOLUTE = instruction.Instruction.build(
        0x8D,
        *instruction.Instruction.store_to_addr_at_pc("a.out"),
    )
    SEC = instruction.Instruction.build(
        0x38,
        instruction.Instruction.step(
            "alu.carry_set",
        ),
    )
    CLC = instruction.Instruction.build(
        0x18,
        instruction.Instruction.step(
            "alu.carry_clear",
        ),
    )
    ADC_IMMEDIATE = instruction.Instruction.build(
        0x69,
        *instruction.Instruction.load_from_pc("alu.lhs.in"),
        instruction.Instruction.step(
            "alu.rhs.in",
            "a.out",
        ),
        instruction.Instruction.step(
            "alu.add",
        ),
        instruction.Instruction.step(
            "alu.result.out",
            "a.in",
        ),
    )

    @classmethod
    def entries(cls) -> frozenset[controller.Controller.Entry]:
        return frozenset().union(*[instruction.value.entries() for instruction in cls])

    def __call__(self, *operands: "program.Value") -> "statement.Statement":
        return operation.Operation(instruction=self, operands=list(operands))


from pycom.computer.programs import statement, operation, program
