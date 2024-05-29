import unittest
import pycom


class StepTest(unittest.TestCase):
    def test_with_controls(self) -> None:
        self.assertEqual(
            pycom.Step().with_controls("a", "b"),
            pycom.Step(controls=frozenset({"a", "b"})),
        )

    def test_entry_no_instruction(self) -> None:
        self.assertEqual(
            pycom.Step()
            .with_controls("a")
            .entry(
                instruction=None,
                instruction_counter=2,
                status_mask=1,
                status_value=1,
            ),
            pycom.Controller.Entry(
                instruction=None,
                instruction_counter=2,
                status_mask=1,
                status_value=1,
                controls=frozenset({"a"}),
            ),
        )
