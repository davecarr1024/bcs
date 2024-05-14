import typing
from . import tristate_buffer
from .. import component, logic
from ... import pin


class Transceiver(component.Component):
    TX = True
    RX = False

    def __init__(
        self,
        size: int,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)
        self.tr = self.add_pin("tr")
        self.enable = self.add_pin("enable")

        tr_inverse = logic.Not(self.tr, "tr_inverse", self).output
        tx_enable = logic.And("tx_enable", self, self.tr, self.enable).output
        rx_enable = logic.And("rx_enable", self, tr_inverse, self.enable).output

        tx_pins: typing.MutableSequence[pin.Pin] = []
        rx_pins: typing.MutableSequence[pin.Pin] = []
        for i in range(size):
            tx_pin = self.add_pin(f"tx_{i}")
            rx_pin = self.add_pin(f"rx_{i}")

            tx_buffer = tristate_buffer.TristateBuffer(f"tx_buffer_{i}", self)
            tx_buffer.enable.connect(tx_enable)
            tx_buffer.input.connect(tx_pin)
            tx_buffer.output.connect(rx_pin)

            rx_buffer = tristate_buffer.TristateBuffer(f"rx_buffer_{i}", self)
            rx_buffer.enable.connect(rx_enable)
            rx_buffer.input.connect(rx_pin)
            rx_buffer.output.connect(rx_pin)

        self.tx_pins: typing.Sequence[pin.Pin] = tx_pins
        self.rx_pins: typing.Sequence[pin.Pin] = rx_pins
