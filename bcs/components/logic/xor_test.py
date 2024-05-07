import unittest

from bcs.components.logic import xor


class XorTest(unittest.TestCase):
    def test_eval(self) -> None:
        for a, b, o in list[tuple[bool, bool, bool]](
            [
                (False, False, False),
                (False, True, True),
                (True, False, True),
                (True, True, False),
            ]
        ):
            with self.subTest(a=a, b=b, o=o):
                c = xor.Xor()
                c["a"].state = a
                c["b"].state = b
                c.run_until_stable()
                self.assertEqual(c["o"].state, o)
