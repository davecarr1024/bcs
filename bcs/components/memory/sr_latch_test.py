import unittest

import bcs


class JKFlipFlopTest(unittest.TestCase):
    def test_set(self) -> None:
        sr_latch = bcs.components.memory.SRLatch()
        sr_latch.states = {
            "s_inverse": False,
            "r_inverse": True,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s_inverse": False,
                "r_inverse": True,
                "q": True,
                "q_inverse": False,
            },
        )
        sr_latch.states = {
            "s_inverse": True,
            "r_inverse": True,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s_inverse": True,
                "r_inverse": True,
                "q": True,
                "q_inverse": False,
            },
        )

    def test_reset(self) -> None:
        sr_latch = bcs.components.memory.SRLatch()
        sr_latch.states = {
            "s_inverse": True,
            "r_inverse": False,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s_inverse": True,
                "r_inverse": False,
                "q": False,
                "q_inverse": True,
            },
        )
        sr_latch.states = {
            "s_inverse": True,
            "r_inverse": True,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s_inverse": True,
                "r_inverse": True,
                "q": False,
                "q_inverse": True,
            },
        )
