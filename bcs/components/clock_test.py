import unittest

from bcs.components import clock


class ClockTest(unittest.TestCase):
    def test_disabled_is_stable(self) -> None:
        c = clock.Clock()
        c["en"].connect_ground()
        c.run_until_stable()

    def test_enabled_is_unstable(self) -> None:
        c = clock.Clock()
        c["en"].connect_power()
        with self.assertRaisesRegex(Exception, "failed to become stable"):
            c.run_until_stable()
