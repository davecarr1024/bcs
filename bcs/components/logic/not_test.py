import unittest

import bcs


class NotTest(unittest.TestCase):
    def test_eval(self) -> None:
        for a, o in list[tuple[bool, bool]]([]):
            with self.subTest(i=a, o=o):
                a_pin = bcs.Pin("a", bcs.components.Component())
                o_pin = ~a_pin
                a_pin.state = a
                self.assertEqual(o_pin.state, o)
