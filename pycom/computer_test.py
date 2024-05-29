import unittest
import pycom


class ComputerTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.computer.Computer()
        self.assertEqual(computer.controller.instruction_counter, 0)

    def test_nop(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.NOP(),
        )
        computer.run_instruction()
        self.assertEqual(computer.controller.instruction_counter, 0)
        self.assertEqual(computer.program_counter, 1)

    def test_lda_immediate(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDA(
                pycom.operands.Immediate(42),
            ),
        )
        computer.run_instruction()
        self.assertEqual(computer.a, 42)

    def test_lda_absolute(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDA(
                    pycom.operands.Absolute(0xBEEF),
                )
            )
            .with_value_at(0xBEEF, 42)
            .as_computer()
        )
        computer.run_instruction()
        self.assertEqual(computer.a, 42)

    def test_lda_absolute_with_label(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDA(
                    pycom.operands.Absolute("value"),
                )
            )
            .at(0xBEEF)
            .with_label("value")
            .with_value(42)
            .as_computer()
        )
        computer.run_instruction()
        self.assertEqual(computer.a, 42)

    def test_sta_absolute(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDA(
                pycom.operands.Immediate(42),
            ),
            pycom.Instructions.STA(
                pycom.operands.Absolute(0xBEEF),
            ),
        )
        computer.run_instructions(2)
        self.assertEqual(computer.memory.data[0xBEEF], 42)

    def test_sta_absolute_label(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDA(
                    pycom.operands.Immediate(42),
                ),
                pycom.Instructions.STA(
                    pycom.operands.Absolute("value"),
                ),
            )
            .with_label_at(0xBEEF, "value")
            .as_computer()
        )
        computer.run_instructions(2)
        self.assertEqual(computer.memory.data[0xBEEF], 42)

    def test_clc(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.CLC(),
        )
        computer.alu.carry = True
        computer.run_instruction()
        self.assertFalse(computer.alu.carry)

    def test_sec(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.SEC(),
        )
        computer.alu.carry = False
        computer.run_instruction()
        self.assertTrue(computer.alu.carry)

    def test_adc_immediate(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDA(
                pycom.operands.Immediate(1),
            ),
            pycom.Instructions.ADC(
                pycom.operands.Immediate(2),
            ),
        )
        computer.run_instructions(2)
        self.assertEqual(computer.a, 3)

    def test_adc_absolute(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDA(
                    pycom.operands.Immediate(1),
                ),
                pycom.Instructions.ADC(
                    pycom.operands.Absolute("value"),
                ),
            )
            .at(0xBEEF)
            .with_label("value")
            .with_value(2)
            .as_computer()
        )
        computer.run()
        self.assertEqual(computer.a, 3)

    def test_jmp_absolute(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.JMP(
                    pycom.operands.Absolute("a"),
                ),
            )
            .with_label_at(0xBEEF, "a")
            .as_computer()
        )
        computer.run_instruction()
        self.assertEqual(
            computer.program_counter,
            0xBEEF,
        )

    def test_bne_true(self) -> None:
        computer = (
            pycom.Program()
            .at(0xBEEF)
            .with_entry(
                pycom.Instructions.BNE(
                    pycom.operands.Relative(0x42),
                ),
            )
            .as_computer()
        )
        computer.alu.zero = True
        computer.program_counter = 0xBEEF
        computer.run_instruction()
        self.assertEqual(
            computer.program_counter,
            0xBE42,
        )

    def test_bne_true_label(self) -> None:
        computer = (
            pycom.Program()
            .at(0xBEEF)
            .with_entry(
                pycom.Instructions.BNE(
                    pycom.operands.Relative("a"),
                ),
            )
            .with_label_at(0xBE42, "a")
            .as_computer()
        )
        computer.alu.zero = True
        computer.program_counter = 0xBEEF
        computer.run_instruction()
        self.assertEqual(
            computer.program_counter,
            0xBE42,
        )

    def test_bne_false(self) -> None:
        computer = (
            pycom.Program()
            .at(0xBEEF)
            .with_entry(
                pycom.Instructions.BNE(
                    pycom.operands.Relative(0x42),
                ),
            )
            .as_computer()
        )
        computer.alu.zero = False
        computer.program_counter = 0xBEEF
        computer.run_instruction()
        self.assertEqual(
            computer.program_counter,
            0xBEEF + 2,
        )

    def test_bne_false_label(self) -> None:
        computer = (
            pycom.Program()
            .at(0xBEEF)
            .with_entry(
                pycom.Instructions.BNE(
                    pycom.operands.Relative("a"),
                ),
            )
            .with_label_at(0xBE42, "a")
            .as_computer()
        )
        computer.alu.zero = False
        computer.program_counter = 0xBEEF
        computer.run_instruction()
        self.assertEqual(
            computer.program_counter,
            0xBEEF + 2,
        )

    def test_ldx_immediate(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDX(pycom.operands.Immediate(1)),
        )
        computer.run_instruction()
        self.assertEqual(computer.x, 1)

    def test_ldx_absolute(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDX(pycom.operands.Absolute("value")),
            )
            .at(0xBEEF)
            .with_label("value")
            .with_value(42)
            .as_computer()
        )
        computer.run_instruction()
        self.assertEqual(computer.x, 42)

    def test_stx_absolute(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDX(pycom.operands.Immediate(42)),
                pycom.Instructions.STX(pycom.operands.Absolute("value")),
            )
            .with_label_at(0xBEEF, "value")
            .as_computer()
        )
        computer.run_instructions(2)
        self.assertEqual(computer.memory.data[0xBEEF], 42)

    def test_inx(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDX(pycom.operands.Immediate(1)),
            pycom.Instructions.INX(),
        )
        computer.run_instructions(2)
        self.assertEqual(computer.x, 2)

    def test_dex(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDX(pycom.operands.Immediate(2)),
            pycom.Instructions.DEX(),
        )
        computer.run_instructions(2)
        self.assertEqual(computer.x, 1)

    def test_ldy_immediate(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDY(pycom.operands.Immediate(1)),
        )
        computer.run_instruction()
        self.assertEqual(computer.y, 1)

    def test_ldy_absolute(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDY(pycom.operands.Absolute("data")),
            "data",
            1,
        )
        computer.run_instruction()
        self.assertEqual(computer.y, 1)

    def test_sty_absolute(self) -> None:
        computer = (
            pycom.Program.build(
                pycom.Instructions.LDY(pycom.operands.Immediate(42)),
                pycom.Instructions.STY(pycom.operands.Absolute("value")),
            )
            .with_label_at(0xBEEF, "value")
            .as_computer()
        )
        computer.run_instructions(2)
        self.assertEqual(computer.memory.data[0xBEEF], 42)

    def test_iny(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDY(pycom.operands.Immediate(1)),
            pycom.Instructions.INY(),
        )
        computer.run_instructions(2)
        self.assertEqual(computer.y, 2)

    def test_dey(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.LDY(pycom.operands.Immediate(2)),
            pycom.Instructions.DEY(),
        )
        computer.run_instructions(2)
        self.assertEqual(computer.y, 1)

    def test_multiply(self) -> None:
        # a = x * y
        computer = pycom.Program.computer(
            pycom.Instructions.LDA(pycom.operands.Immediate(0)),
            pycom.Instructions.LDX(pycom.operands.Immediate(3)),
            pycom.Instructions.LDY(pycom.operands.Immediate(5)),
            "loop",
            pycom.Instructions.STY(pycom.operands.Absolute("tmp")),
            pycom.Instructions.ADC(pycom.operands.Absolute("tmp")),
            pycom.Instructions.DEX(),
            pycom.Instructions.BNE(pycom.operands.Relative("done")),
            pycom.Instructions.JMP(pycom.operands.Absolute("loop")),
            "done",
            pycom.Instructions.HLT(),
            "tmp",
        )
        computer.run()
        self.assertEqual(computer.a, 15)
