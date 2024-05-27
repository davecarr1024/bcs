import unittest

import pycom


class StepTest(unittest.TestCase):
    def test_with_controls(self) -> None:
        self.assertEqual(
            pycom.computer.Step().with_controls("a", "b"),
            pycom.computer.Step(controls=frozenset({"a", "b"})),
        )

    def test_with_status(self) -> None:
        self.assertEqual(
            pycom.computer.Step().with_status(0x1, False).with_status(0x2, True),
            pycom.computer.Step(status_mask=0x3, status_value=0x2),
        )

    def test_entry_with_instruction(self) -> None:
        self.assertEqual(
            pycom.computer.Step()
            .with_controls("a")
            .with_status(1, True)
            .entry(
                instruction=1,
                instruction_counter=2,
            ),
            pycom.Controller.Entry(
                instruction=1,
                instruction_counter=2,
                status_mask=1,
                status_value=1,
                controls=frozenset({"a"}),
            ),
        )

    def test_entry_no_instruction(self) -> None:
        self.assertEqual(
            pycom.computer.Step()
            .with_controls("a")
            .with_status(1, True)
            .entry(
                instruction=None,
                instruction_counter=2,
            ),
            pycom.Controller.Entry(
                instruction=None,
                instruction_counter=2,
                status_mask=1,
                status_value=1,
                controls=frozenset({"a"}),
            ),
        )
