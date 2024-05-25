import unittest
import pycom


class ComputerTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.Computer()
        self.assertEqual(computer.controller.instruction_counter, 0)

    def test_nop(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_value(
                pycom.Computer.Opcode.NOP,
            )
            .computer()
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.controller.instruction_counter, 0)
        self.assertEqual(computer.program_counter, 1)

    def test_lda_immediate(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_values(
                pycom.Computer.Opcode.LDA_IMMEDIATE,
                2,
            )
            .computer()
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a, 2)

    def test_lda_memory(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_values(
                pycom.Computer.Opcode.LDA_ABSOLUTE,
                0xBE,
                0xEF,
            )
            .with_value_at(
                0xBEEF,
                42,
            )
            .computer()
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a, 42)

    def test_sta_memory(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_values(
                pycom.Computer.Opcode.LDA_IMMEDIATE,
                42,
            )
            .with_values(
                pycom.Computer.Opcode.STA_ABSOLUTE,
                0xBE,
                0xEF,
            )
            .computer()
        )
        computer.controller.run_instructions(2)
        self.assertEqual(
            computer.memory.data[0xBEEF],
            42,
        )

    def test_clc(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_value(
                pycom.Computer.Opcode.CLC,
            )
            .computer()
        )
        computer.alu.carry = True
        computer.run_instruction()
        self.assertFalse(computer.alu.carry)

    def test_sec(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_value(
                pycom.Computer.Opcode.SEC,
            )
            .computer()
        )
        computer.alu.carry = False
        computer.run_instruction()
        self.assertTrue(computer.alu.carry)

    def test_adc_immediate(self) -> None:
        computer = (
            pycom.Computer.Program()
            .with_values(
                pycom.Computer.Opcode.LDA_IMMEDIATE,
                1,
            )
            .with_values(
                pycom.Computer.Opcode.ADC_IMMEDIATE,
                2,
            )
            .computer()
        )
        computer.run_instructions(2)
        self.assertEqual(computer.a, 3)
