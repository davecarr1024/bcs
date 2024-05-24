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
            controller.state,
            pycom.Controller.State(
                1,
                2,
            ),
        )
