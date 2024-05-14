import unittest

import bcs


class EdgeDetectorTest(unittest.TestCase):
    def test_eval(self) -> None:
        input = bcs.Pin("input", bcs.components.Component())
        ed = bcs.components.clock.EdgeDetector(input)
        input.state = False
        self.assertFalse(ed.output.state)
        input.state = True
        self.assertTrue(ed.output.state)
        ed.update_all()
        self.assertFalse(ed.output.state)
