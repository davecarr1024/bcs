import unittest

import pycom


class ClockTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.HLT(),
        )
        self.assertEqual(
            computer.run(),
            len(pycom.Instruction._preamble()) + 1,
        )

    def test_empty_default_hlt(self) -> None:
        computer = pycom.Program.computer()
        self.assertEqual(
            computer.run(),
            len(pycom.Instruction._preamble()) + 1,
        )

    def test_nops(self) -> None:
        computer = pycom.Program.computer(
            pycom.Instructions.NOP(),
            pycom.Instructions.NOP(),
            pycom.Instructions.NOP(),
            pycom.Instructions.HLT(),
        )
        self.assertEqual(
            computer.run(),
            (len(pycom.Instruction._preamble()) + 1) * 4,
        )
