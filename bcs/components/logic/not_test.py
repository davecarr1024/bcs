import unittest

from bcs.components.logic import not_


class NotTest(unittest.TestCase):
    def test_eval(self) -> None:
        for a, o in list[tuple[bool, bool]](
            [
                (True, False),
                (False, True),
            ]
        ):
            with self.subTest(a=a, o=o):
                c = not_.Not()
                c["a"].state = a
                c["o"].run_until_state(o)
