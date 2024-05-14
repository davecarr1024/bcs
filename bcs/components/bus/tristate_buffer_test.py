import unittest

import bcs


class TristateBufferTest(unittest.TestCase):
    def test_enable(self) -> None:
        tb = bcs.components.bus.TristateBuffer()
        tb.states = dict(
            enable=True,
            input=True,
        )
        self.assertDictEqual(
            tb.states,
            dict(
                enable=True,
                input=True,
                output=True,
            ),
        )
        tb.states = dict(
            enable=True,
            input=False,
            output=False,
        )

    def test_disable(self) -> None:
        tb = bcs.components.bus.TristateBuffer()
        tb.states = dict(
            enable=True,
            input=True,
        )
        self.assertDictEqual(
            tb.states,
            dict(
                enable=True,
                input=True,
                output=True,
            ),
        )
        tb.enable.state = False
        tb.input.state = False
        self.assertDictEqual(
            tb.states,
            dict(
                enable=False,
                input=False,
                output=True,
            ),
        )
