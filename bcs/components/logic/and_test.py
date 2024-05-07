import unittest

from bcs.components.logic import and_


class AndTest(unittest.TestCase):
    def test_eval(self) -> None:
        for a, b, o in list[tuple[bool, bool, bool]](
            [
                (False, False, False),
                (False, True, False),
                (True, False, False),
                (True, True, True),
            ]
        ):
            with self.subTest(a=a, b=b, o=o):
                c = and_.And()
                c["a"].state = a
                c["b"].state = b
                c.run_until_stable()
                self.assertEqual(c["o"].state, o)
