import typing
import unittest

import bcs


class ClockTest(unittest.TestCase):
    def test_disabled(self) -> None:
        clk = bcs.components.power.Clock()
        clk.enable.state = False
        clk.update()
        self.assertFalse(clk.output.state)
        clk.update()
        self.assertFalse(clk.output.state)
        clk.update()
        self.assertFalse(clk.output.state)

    def test_enabled(self) -> None:
        clk = bcs.components.power.Clock()
        clk.enable.state = True
        clk.update()
        self.assertFalse(clk.output.state)
        clk.update()
        self.assertTrue(clk.output.state)
        clk.update()
        self.assertFalse(clk.output.state)
        clk.update()
        self.assertTrue(clk.output.state)

    def test_pulse(self) -> None:
        class PulseRecorder(bcs.components.Component):
            def __init__(self) -> None:
                super().__init__()
                self.clk_states: typing.MutableSequence[bool] = []
                self.clk = self.add_pin("clk")

            def update(self) -> None:
                clk_state = self.clk.state
                print(f"got clk_state {clk_state}")
                if not self.clk_states or self.clk_states[-1] != clk_state:
                    self.clk_states.append(clk_state)

        pulse_recorder = PulseRecorder()
        clk = bcs.components.power.Clock()
        clk.output.connect(pulse_recorder.clk)
        clk.pulse()
        self.assertSequenceEqual(pulse_recorder.clk_states[-2:], [True, False])
