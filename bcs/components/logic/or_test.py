import unittest

import bcs


class OrTest(unittest.TestCase):
    def test_eval(self) -> None:
        for a, b, o in list[tuple[bool, bool, bool]](
            [
                (False, False, False),
                (False, True, True),
                (True, False, True),
                (True, True, True),
            ]
        ):
            with self.subTest(a=a, b=b, o=o):
                a_pin = bcs.components.Component("ac").add_pin("a")
                b_pin = bcs.components.Component("bc").add_pin("b")
                or_ = a_pin | b_pin
                a_pin.state = a
                b_pin.state = b
                self.assertEqual(or_.state, o)
