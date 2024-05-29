import unittest
import pycom


class NoneTest(unittest.TestCase):
    def test_statement(self) -> None:
        self.assertEqual(
            pycom.Program().with_statement(
                pycom.operands.None_().statement(1),
            ),
            pycom.Program().with_value(
                pycom.references.Literal(1),
            ),
        )
