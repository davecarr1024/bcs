import unittest
import pycom


class AbsoluteTest(unittest.TestCase):
    def test_statement_int(self) -> None:
        self.assertEqual(
            pycom.computer.Program.build(
                pycom.computer.operands.Absolute(0xBEEF).statement(2),
            ),
            pycom.computer.Program().with_values(2, 0xBE, 0xEF),
        )

    def test_statement_str(self) -> None:
        self.assertEqual(
            pycom.computer.Program.build(
                pycom.computer.operands.Absolute("a").statement(2),
            ),
            pycom.computer.Program().with_values(2, "a"),
        )
