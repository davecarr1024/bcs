import unittest
import pycom


class AbsoluteTest(unittest.TestCase):
    def test_statement(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.operands.Absolute(0xBEEF).statement(2),
            ),
            pycom.computer.Program().with_values(2, 0xBE, 0xEF),
        )
