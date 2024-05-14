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
        sr_latch.states = {
            "s": True,
            "r": False,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": True,
                "r": False,
                "q": True,
                "q_inverse": False,
            },
        )
        sr_latch.states = {
            "s": False,
            "r": False,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": False,
                "r": False,
                "q": True,
                "q_inverse": False,
            },
        )

    def test_reset(self) -> None:
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
        sr_latch.states = {
            "s": False,
            "r": True,
        }
        self.assertDictEqual(
            sr_latch.states,
            {
                "s": False,
                "r": True,
                "q": False,
                "q_inverse": True,
            },
        )
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
                "q_inverse": True,
            },
        )
