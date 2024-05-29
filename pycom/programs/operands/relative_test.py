import unittest
import pycom


class RelativeTest(unittest.TestCase):
    def test_statement_literal(self) -> None:
        self.assertEqual(
            pycom.Program().with_statement(
                pycom.operands.Relative(1).statement(2),
            ),
            pycom.Program().with_values(
                pycom.references.Literal(2),
                pycom.references.Literal(1),
            ),
        )

    def test_statement_label(self) -> None:
        self.assertEqual(
            pycom.Program().with_statement(
                pycom.operands.Relative("a").statement(2),
            ),
            pycom.Program().with_values(
                pycom.references.Literal(2),
                pycom.references.Relative("a"),
            ),
        )
