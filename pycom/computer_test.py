import unittest

import pycom


class ComputerTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.Computer()
        self.assertEqual(computer.program_counter.value, 0)
        self.assertEqual(computer.controller.instruction_counter, pycom.Byte(0))

    def test_nop(self) -> None:
        computer = pycom.Computer()
        self.assertEqual(computer.controller.run_instruction(), 4)
        self.assertEqual(computer.controller.instruction_counter, pycom.Byte(0))
        self.assertEqual(computer.program_counter.value, 1)

    def test_lda_immediate(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Byte(1),
                1: pycom.Byte(2),
            }
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a.value, pycom.Byte(2))

    def test_lda_memory(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Byte(2),
                1: pycom.Byte(0xBE),
                2: pycom.Byte(0xEF),
                0xBEEF: pycom.Byte(42),
            }
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a.value, pycom.Byte(42))

    def test_sta_memory(self) -> None:
        computer = pycom.Computer(
            data={
                0: pycom.Byte(1),
                1: pycom.Byte(42),
                2: pycom.Byte(3),
                3: pycom.Byte(0xBE),
                4: pycom.Byte(0xEF),
            }
        )
        computer.controller.run_instructions(2)
        self.assertEqual(
            computer.memory.data[0xBEEF],
            pycom.Byte(42),
        )
