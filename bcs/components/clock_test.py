import unittest

from bcs.components import clock


class ClockTest(unittest.TestCase):
    def test_unstable(self) -> None:
        c = clock.Clock()
        with self.assertRaisesRegex(Exception, "failed to become stable"):
            c.run_until_stable()
