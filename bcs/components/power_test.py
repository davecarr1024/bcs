import unittest

import bcs


class PowerTest(unittest.TestCase):
    def test_stable(self) -> None:
        bcs.components.Power()["o"].run_until_stable_with_state(True)
