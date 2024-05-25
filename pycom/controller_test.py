import unittest

import pycom


class ControllerTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Controller(pycom.Bus(), frozenset())

    def test_get_state(self) -> None:
        controller = pycom.Controller(pycom.Bus(), frozenset())
        controller.instruction_buffer = 1
        controller.instruction_counter = 2
        self.assertEqual(
            controller.state(3),
            pycom.Controller.State(
                instruction=1,
                instruction_counter=2,
                status=3,
            ),
        )

    def test_entry_matches(self) -> None:
        for state, entry, expected in list[
            tuple[
                pycom.Controller.State,
                pycom.Controller.Entry,
                bool,
            ]
        ](
            [
                (
                    pycom.Controller.State(
                        instruction=1,
                        instruction_counter=2,
                        status=3,
                    ),
                    pycom.Controller.Entry(),
                    True,
                ),
                (
                    pycom.Controller.State(
                        instruction=1,
                        instruction_counter=2,
                        status=3,
                    ),
                    pycom.Controller.Entry(
                        instruction=1,
                    ),
                    True,
                ),
                (
                    pycom.Controller.State(
                        instruction=1,
                        instruction_counter=2,
                        status=3,
                    ),
                    pycom.Controller.Entry(
                        instruction=3,
                    ),
                    False,
                ),
                (
                    pycom.Controller.State(
                        instruction=1,
                        instruction_counter=2,
                        status=3,
                    ),
                    pycom.Controller.Entry(
                        instruction_counter=2,
                    ),
                    True,
                ),
                (
                    pycom.Controller.State(
                        instruction=1,
                        instruction_counter=2,
                        status=3,
                    ),
                    pycom.Controller.Entry(
                        instruction_counter=3,
                    ),
                    False,
                ),
            ]
        ):
            with self.subTest(
                state=state,
                entry=entry,
                expected=expected,
            ):
                self.assertEqual(
                    entry.matches(state),
                    expected,
                )

    def test_get_entry(self) -> None:
        a = pycom.Controller.Entry(
            instruction=1,
            instruction_counter=2,
            controls=frozenset({"a"}),
        )
        b = pycom.Controller.Entry(
            instruction=3,
            instruction_counter=4,
            controls=frozenset({"b"}),
        )
        controller = pycom.Controller(pycom.Bus(), entries=frozenset({a, b}))
        controller.instruction_buffer = 1
        controller.instruction_counter = 2
        self.assertEqual(controller.entry(3), a)
        controller.instruction_buffer = 3
        controller.instruction_counter = 4
        self.assertEqual(controller.entry(3), b)

    def test_get_entry_not_found(self) -> None:
        with self.assertRaises(pycom.Controller.EntryError):
            pycom.Controller(pycom.Bus(), entries=frozenset()).entry(3)

    def test_get_entry_multiple_found(self) -> None:
        with self.assertRaises(pycom.Controller.EntryError):
            pycom.Controller(
                pycom.Bus(),
                entries=frozenset(
                    {
                        pycom.Controller.Entry(controls=frozenset({"a"})),
                        pycom.Controller.Entry(controls=frozenset({"b"})),
                    }
                ),
            ).entry(3)
