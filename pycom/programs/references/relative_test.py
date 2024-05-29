import unittest
import pycom


class RelativeTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.Program().with_label_at(0xBEEF, "a")
        self.assertEqual(
            pycom.references.Relative("a")(
                pycom.Program.Output(
                    program,
                ),
                0xBE00,
            ),
            pycom.Program.Output(program).with_values_at(0xBE00, 0xEF),
        )

    def test_call_not_found(self) -> None:
        program = pycom.Program()
        with self.assertRaises(pycom.Program.LabelNotFoundError):
            pycom.references.Relative("a")(
                pycom.Program.Output(
                    program,
                ),
                0,
            )

    def test_call_out_of_range(self) -> None:
        program = pycom.Program().with_label_at(0xBEEF, "a")
        with self.assertRaises(pycom.references.Relative.AddressNotLocalError):
            pycom.references.Relative("a")(
                pycom.Program.Output(
                    program,
                ),
                0,
            )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.references.Relative.size(),
            1,
        )
