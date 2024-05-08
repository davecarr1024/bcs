import unittest

import bcs


class EdgeDetectorTest(unittest.TestCase):
    def test_detect(self) -> None:
        ed = bcs.components.EdgeDetector()
        ed["a"].state = True
        ed.run_until_states(a=True, o=False, max_t=0.1)
        ed.run_until_states(a=True, o=True, max_t=0.1)
        ed.run_until_states(a=True, o=False, max_t=0.1)
