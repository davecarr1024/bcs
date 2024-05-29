import unittest
import pycom


class AbsoluteTest(unittest.TestCase):
    def test_statement_literal(self) -> None:
        self.assertEqual(
            pycom.Program.build(
                pycom.operands.Absolute(0xBEEF).statement(2),
            ),
            pycom.Program().with_values(
                pycom.references.Literal(2),
                pycom.references.Pair.for_value(0xBEEF),
            ),
        )

    def test_statement_label(self) -> None:
        self.assertEqual(
            pycom.Program.build(
                pycom.operands.Absolute("a").statement(2),
            ),
            pycom.Program().with_values(
                pycom.references.Literal(2),
                pycom.references.Absolute("a"),
            ),
        )
