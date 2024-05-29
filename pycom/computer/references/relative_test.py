import unittest
import pycom


class RelativeTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.computer.Program().with_label_at(0xBEEF, "a")
        self.assertEqual(
            pycom.computer.references.Relative("a")(
                pycom.computer.Program.Output(
                    program,
                ),
                0xBE00,
            ),
            pycom.computer.Program.Output(program).with_values_at(0xBE00, 0xEF),
        )

    def test_call_not_found(self) -> None:
        program = pycom.computer.Program()
        with self.assertRaises(pycom.computer.Program.LabelNotFoundError):
            pycom.computer.references.Relative("a")(
                pycom.computer.Program.Output(
                    program,
                ),
                0,
            )

    def test_call_out_of_range(self) -> None:
        program = pycom.computer.Program().with_label_at(0xBEEF, "a")
        with self.assertRaises(pycom.computer.references.Relative.AddressNotLocalError):
            pycom.computer.references.Relative("a")(
                pycom.computer.Program.Output(
                    program,
                ),
                0,
            )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.computer.references.Relative.size(),
            1,
        )
