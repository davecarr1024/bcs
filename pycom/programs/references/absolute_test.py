import unittest
import pycom


class AbsoluteTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.Program().with_label_at(0xBEEF, "a")
        self.assertEqual(
            pycom.references.Absolute("a")(
                pycom.Program.Output(
                    program,
                ),
                0,
            ),
            pycom.Program.Output(program).with_values_at(0, 0xBE, 0xEF),
        )

    def test_call_not_found(self) -> None:
        program = pycom.Program()
        with self.assertRaises(pycom.Program.LabelNotFoundError):
            pycom.references.Absolute("a")(
                pycom.Program.Output(
                    program,
                ),
                0,
            )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.references.Absolute.size(),
            2,
        )
