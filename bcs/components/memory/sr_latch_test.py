import unittest

import bcs


class JKFlipFlopTest(unittest.TestCase):
    def test_empty(self) -> None:
        sr_latch = bcs.components.memory.SRLatch()
        sr_latch.states = {
            "s": False,
            "r": False,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": False,
                "r": False,
                "q": False,
                "q_inverse": False,
            },
        )

    def test_set(self) -> None:
        print("\n\ntest_set")
        sr_latch = bcs.components.memory.SRLatch()
        print("\n\nunset")
        sr_latch.states = {
            "s": False,
            "r": False,
        }
        print("\n\n/unset")
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": False,
                "r": False,
                "q": False,
                "q_inverse": False,
            },
        )
        print("\n\nset")
        sr_latch.states = {
            "s": True,
            "r": False,
        }
        print("\n\n/set")
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": True,
                "r": False,
                "q": True,
                "q_inverse": False,
            },
        )
        print("\n\nset")
        sr_latch.states = {
            "s": False,
            "r": False,
        }
        print("\n\n/set")
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": False,
                "r": False,
                "q": True,
                "q_inverse": False,
            },
        )
