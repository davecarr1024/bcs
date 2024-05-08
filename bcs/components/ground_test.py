import unittest

import bcs


class GroundTest(unittest.TestCase):
    def test_stable(self) -> None:
        bcs.components.Ground()["o"].run_until_stable_with_state(False)
