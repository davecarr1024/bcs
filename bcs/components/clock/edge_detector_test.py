import unittest

import bcs


class EdgeDetectorTest(unittest.TestCase):
    def test_eval(self) -> None:
        ed = bcs.components.clock.EdgeDetector()
        ed.input.state = False
        self.assertFalse(ed.output.state)
        ed.input.state = True
        self.assertTrue(ed.output.state)
        ed.update_all()
        self.assertFalse(ed.output.state)
