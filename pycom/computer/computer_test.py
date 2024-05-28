import unittest
import pycom


class ComputerTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.computer.Computer()
        self.assertEqual(computer.controller.instruction_counter, 0)

    def test_nop(self) -> None:
        computer = pycom.computer.Program.computer(
            pycom.computer.Instructions.NOP(),
        )
        computer.run_instruction()
        self.assertEqual(computer.controller.instruction_counter, 0)
        self.assertEqual(computer.program_counter, 1)

    def test_lda_immediate(self) -> None:
        computer = pycom.computer.Program.computer(
            pycom.computer.Instructions.LDA(
                pycom.computer.operands.Immediate(42),
            ),
        )
        computer.run_instruction()
        self.assertEqual(computer.a, 42)

    def test_lda_absolute(self) -> None:
        computer = (
            pycom.computer.Program.build(
                pycom.computer.Instructions.LDA(
                    pycom.computer.operands.Absolute(0xBEEF),
                )
            )
            .with_value_at(0xBEEF, 42)
            .as_computer()
        )
        computer.run_instruction()
        self.assertEqual(computer.a, 42)

    # def test_lda_absolute_with_label(self) -> None:
    #     computer = (
    #         pycom.computer.Program.build(
    #             pycom.computer.Instructions.LDA_ABSOLUTE("value"),
    #         )
    #         .at(0xBEEF)
    #         .with_label("value")
    #         .with_value(42)
    #         .as_computer()
    #     )
    #     computer.run_instruction()
    #     self.assertEqual(computer.a, 42)

    # def test_sta_absolute(self) -> None:
    #     computer = pycom.computer.Program.computer(
    #         pycom.computer.Instructions.LDA_IMMEDIATE(42),
    #         pycom.computer.Instructions.STA_ABSOLUTE(0xBE, 0xEF),
    #     )
    #     computer.run_instructions(2)
    #     self.assertEqual(computer.memory.data[0xBEEF], 42)

    # def test_sta_absolute_label(self) -> None:
    #     computer = (
    #         pycom.computer.Program.build(
    #             pycom.computer.Instructions.LDA_IMMEDIATE(42),
    #             pycom.computer.Instructions.STA_ABSOLUTE("value"),
    #         )
    #         .at(0xBEEF)
    #         .with_label("value")
    #         .as_computer()
    #     )
    #     computer.run_instructions(2)
    #     self.assertEqual(computer.memory.data[0xBEEF], 42)

    # def test_clc(self) -> None:
    #     computer = pycom.computer.Program.computer(
    #         pycom.computer.Instructions.CLC(),
    #     )
    #     computer.alu.carry = True
    #     computer.run_instruction()
    #     self.assertFalse(computer.alu.carry)

    # def test_sec(self) -> None:
    #     computer = pycom.computer.Program.computer(
    #         pycom.computer.Instructions.SEC(),
    #     )
    #     computer.alu.carry = False
    #     computer.run_instruction()
    #     self.assertTrue(computer.alu.carry)

    # def test_adc_immediate(self) -> None:
    #     computer = pycom.computer.Program.computer(
    #         pycom.computer.Instructions.LDA_IMMEDIATE(1),
    #         pycom.computer.Instructions.ADC_IMMEDIATE(2),
    #     )
    #     computer.run_instructions(2)
    #     self.assertEqual(computer.a, 3)

    # def test_jmp_absolute(self) -> None:
    #     computer = (
    #         pycom.computer.Program.build(
    #             pycom.computer.Instructions.JMP_ABSOLUTE("a"),
    #         )
    #         .at(0xBEEF)
    #         .with_label("a")
    #         .as_computer()
    #     )
    #     computer.run_instruction()
    #     self.assertEqual(
    #         computer.program_counter,
    #         0xBEEF,
    #     )

    # def test_bne_true(self) -> None:
    #     computer = pycom.computer.Program.computer(
    #         pycom.computer.Instructions.BNE(0x42),
    #     )
    #     computer.alu.zero = True
    #     computer.run_instruction()
    #     self.assertEqual(
    #         computer.program_counter,
    #         0x42,
    #     )

    # def test_bne_false(self) -> None:
    #     computer = pycom.computer.Program.computer(
    #         pycom.computer.Instructions.BNE(0x42),
    #     )
    #     computer.alu.zero = False
    #     computer.run_instruction()
    #     self.assertEqual(
    #         computer.program_counter,
    #         0x2,
    #     )
