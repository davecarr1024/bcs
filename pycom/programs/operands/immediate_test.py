import unittest
import pycom


class ImmediateTest(unittest.TestCase):
    def test_statement(self) -> None:
        self.assertEqual(
            pycom.Program().with_statement(
                pycom.operands.Immediate(1).statement(2),
            ),
            pycom.Program().with_values(
                pycom.references.Literal(2),
                pycom.references.Literal(1),
            ),
        )
