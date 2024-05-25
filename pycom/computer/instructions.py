import enum
from pycom import controller
from pycom.computer import instruction, simple_instruction


class Instructions(enum.Enum):
    NOP = simple_instruction.SimpleInstruction.build(
        0xEA,
    )
    LDA_IMMEDIATE = simple_instruction.SimpleInstruction.build(
        0xA9,
        *instruction.Instruction.load_from_pc("a.in"),
    )
    LDA_ABSOLUTE = simple_instruction.SimpleInstruction.build(
        0xAD,
        *instruction.Instruction.load_from_addr_at_pc("a.in"),
    )
    STA_ABSOLUTE = simple_instruction.SimpleInstruction.build(
        0x8D,
        *instruction.Instruction.store_to_addr_at_pc("a.out"),
    )
    SEC = simple_instruction.SimpleInstruction.build(
        0x38,
        instruction.Instruction.step(
            "alu.carry_set",
        ),
    )
    CLC = simple_instruction.SimpleInstruction.build(
        0x18,
        instruction.Instruction.step(
            "alu.carry_clear",
        ),
    )
    ADC_IMMEDIATE = simple_instruction.SimpleInstruction.build(
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
