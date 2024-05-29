import enum
import typing
from pycom.components import alu, byte, controller, errorable
from pycom.programs import operands
from pycom.instructions import instruction


class DuplicateOpcodeError(errorable.Errorable.Error): ...


class Instructions(errorable.Errorable, enum.Enum):
    NOP = instruction.Instruction.build(
        opcode=0xEA,
        operand_type=operands.None_,
        steps=[],
    )
    LDA = (
        instruction.Instruction()
        .with_instance(
            operand_type=operands.Immediate,
            opcode=0xA9,
            steps=instruction.Instruction.load_from_pc("a.in"),
        )
        .with_instance(
            operand_type=operands.Absolute,
            opcode=0xAD,
            steps=instruction.Instruction.load_from_addr_at_pc("a.in"),
        )
    )
    STA = instruction.Instruction().with_instance(
        operand_type=operands.Absolute,
        opcode=0x8D,
        steps=instruction.Instruction.store_to_addr_at_pc("a.out"),
    )
    SEC = instruction.Instruction.build(
        opcode=0x38,
        operand_type=operands.None_,
        steps=[
            instruction.Instruction.step(
                "alu.carry_set",
            )
        ],
    )
    CLC = instruction.Instruction.build(
        opcode=0x18,
        operand_type=operands.None_,
        steps=[
            instruction.Instruction.step(
                "alu.carry_clear",
            )
        ],
    )
    ADC = instruction.Instruction().with_instance(
        operand_type=operands.Immediate,
        opcode=0x69,
        steps=instruction.Instruction.steps(
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
        ),
    )
    JMP = instruction.Instruction().with_instance(
        operand_type=operands.Absolute,
        opcode=0x4C,
        steps=instruction.Instruction.steps(
            *instruction.Instruction.load_from_pc("controller.address_buffer.in"),
            *instruction.Instruction.load_from_pc("program_counter.low_byte.in"),
            instruction.Instruction.step(
                "controller.address_buffer.out",
                "program_counter.high_byte.in",
            ),
        ),
    )
    BNE = instruction.Instruction().with_operand_instance(
        operands.Relative,
        instruction.Instruction.OperandInstance(
            opcode=0xD0,
        )
        .with_status_instance(
            status_mask=alu.ALU.ZERO,
            status_value=alu.ALU.ZERO,
            steps=instruction.Instruction.load_from_pc("program_counter.low_byte.in"),
        )
        .with_status_instance(
            status_mask=alu.ALU.ZERO,
            status_value=0,
            steps=[
                instruction.Instruction.step("program_counter.increment"),
            ],
        ),
    )
    LDX = (
        instruction.Instruction()
        .with_instance(
            opcode=0xA2,
            operand_type=operands.Immediate,
            steps=instruction.Instruction.load_from_pc("x.in"),
        )
        .with_instance(
            opcode=0xAE,
            operand_type=operands.Absolute,
            steps=instruction.Instruction.load_from_addr_at_pc("x.in"),
        )
    )
    STX = instruction.Instruction().with_instance(
        opcode=0x8E,
        operand_type=operands.Absolute,
        steps=instruction.Instruction.store_to_addr_at_pc("x.out"),
    )
    INX = instruction.Instruction.build(
        opcode=0xE8,
        operand_type=operands.None_,
        steps=instruction.Instruction.steps(
            instruction.Instruction.step(
                "x.out",
                "alu.lhs.in",
            ),
            instruction.Instruction.step(
                "alu.inc",
            ),
            instruction.Instruction.step(
                "alu.result.out",
                "x.in",
            ),
        ),
    )
    DEX = instruction.Instruction.build(
        opcode=0xCA,
        operand_type=operands.None_,
        steps=instruction.Instruction.steps(
            instruction.Instruction.step(
                "x.out",
                "alu.lhs.in",
            ),
            instruction.Instruction.step(
                "alu.dec",
            ),
            instruction.Instruction.step(
                "alu.result.out",
                "x.in",
            ),
        ),
    )
    LDY = (
        instruction.Instruction()
        .with_instance(
            opcode=0xA0,
            operand_type=operands.Immediate,
            steps=instruction.Instruction.load_from_pc("y.in"),
        )
        .with_instance(
            opcode=0xAC,
            operand_type=operands.Absolute,
            steps=instruction.Instruction.load_from_addr_at_pc("y.in"),
        )
    )
    STY = instruction.Instruction().with_instance(
        opcode=0x8C,
        operand_type=operands.Absolute,
        steps=instruction.Instruction.store_to_addr_at_pc("y.out"),
    )
    INY = instruction.Instruction.build(
        opcode=0xC8,
        operand_type=operands.None_,
        steps=instruction.Instruction.steps(
            instruction.Instruction.step(
                "y.out",
                "alu.lhs.in",
            ),
            instruction.Instruction.step(
                "alu.inc",
            ),
            instruction.Instruction.step(
                "alu.result.out",
                "y.in",
            ),
        ),
    )
    DEY = instruction.Instruction.build(
        opcode=0x88,
        operand_type=operands.None_,
        steps=instruction.Instruction.steps(
            instruction.Instruction.step(
                "y.out",
                "alu.lhs.in",
            ),
            instruction.Instruction.step(
                "alu.dec",
            ),
            instruction.Instruction.step(
                "alu.result.out",
                "y.in",
            ),
        ),
    )

    @classmethod
    def validate(cls) -> None:
        opcodes: list[int] = sum(
            [list(instruction.value.opcodes) for instruction in cls], []
        )
        duplicate_opcodes: frozenset[int] = frozenset(
            opcode for opcode in opcodes if opcodes.count(opcode) > 1
        )
        if duplicate_opcodes:
            raise DuplicateOpcodeError(
                f"{[byte.Byte.hex_str(opcode) for opcode in duplicate_opcodes]}"
            )

    @classmethod
    def entries(cls) -> frozenset[controller.Controller.Entry]:
        cls.validate()
        return frozenset().union(*[instruction.value.entries() for instruction in cls])

    @typing.overload
    def __call__(self) -> "statement.Statement": ...

    @typing.overload
    def __call__(self, operand: operands.Operand) -> "statement.Statement": ...

    def __call__(
        self,
        operand: typing.Optional[operands.Operand] = None,
    ) -> "statement.Statement":
        return self.value.statement(operand or operands.None_())


from pycom.programs import statement
