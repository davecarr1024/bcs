import unittest
import pycom


class AbsoluteTest(unittest.TestCase):
    def test_statement_literal(self) -> None:
        self.assertEqual(
            pycom.computer.Program.build(
                pycom.computer.operands.Absolute(0xBEEF).statement(2),
            ),
            pycom.computer.Program().with_values(
                pycom.computer.references.Literal(2),
                pycom.computer.references.Pair.for_value(0xBEEF),
            ),
        )

    def test_statement_label(self) -> None:
        self.assertEqual(
            pycom.computer.Program.build(
                pycom.computer.operands.Absolute("a").statement(2),
            ),
            pycom.computer.Program().with_values(
                pycom.computer.references.Literal(2),
                pycom.computer.references.Absolute("a"),
            ),
        )
