import unittest
import pycom


class ComputerTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.Computer()
        self.assertEqual(computer.program_counter.value, 0)
        self.assertEqual(computer.controller.instruction_counter, pycom.Byte(0))

    def test_nop(self) -> None:
        computer = pycom.Computer(data={0: pycom.Computer.NOP})
        computer.controller.run_instruction()
        self.assertEqual(computer.controller.instruction_counter, pycom.Byte(0))
        self.assertEqual(computer.program_counter.value, 1)

    def test_lda_immediate(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Computer.LDA_IMMEDIATE,
                1: 2,
            }
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a, 2)

    def test_lda_memory(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Computer.LDA_ABSOLUTE,
                1: 0xBE,
                2: 0xEF,
                0xBEEF: 42,
            }
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a, 42)

    def test_sta_memory(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Computer.LDA_IMMEDIATE,
                1: 42,
                2: pycom.Computer.STA_ABSOLUTE,
                3: 0xBE,
                4: 0xEF,
            }
        )
        computer.controller.run_instructions(2)
        self.assertEqual(
            computer.memory.data[0xBEEF],
            42,
        )

    def test_clc(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Computer.CLC,
            }
        )
        computer.alu.carry = True
        computer.run_instruction()
        self.assertFalse(computer.alu.carry)

    def test_sec(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Computer.SEC,
            }
        )
        computer.alu.carry = False
        computer.run_instruction()
        self.assertTrue(computer.alu.carry)

    def test_adc_immediate(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Computer.LDA_IMMEDIATE,
                1: 1,
                2: pycom.Computer.ADC_IMMEDIATE,
                3: 2,
            }
        )
        computer.run_instructions(2)
        self.assertEqual(computer.a, 3)
