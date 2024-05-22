import unittest

import pycom


class ControllerTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Controller(pycom.Bus(), frozenset())

    def test_get_state(self) -> None:
        controller = pycom.Controller(pycom.Bus(), frozenset())
        controller.instruction_buffer = pycom.Byte(1)
        controller.instruction_counter = pycom.Byte(2)
        self.assertEqual(
            controller.state,
            pycom.Controller.State(
                pycom.Byte(1),
                pycom.Byte(2),
            ),
        )
