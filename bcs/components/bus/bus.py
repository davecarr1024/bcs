import typing
from .. import component
from ... import pin


class Bus(component.Component):
    def __init__(
        self,
        size: int,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)
        self.channels: typing.Sequence[pin.Pin] = [
            self.add_pin(f"channel_{i}") for i in range(size)
        ]

    @property
    def value(self) -> int:
        value = 0
        for i, channel in enumerate(self.channels):
            value |= int(channel.state) << i
        return value

    @value.setter
    def value(self, value: int) -> None:
        for i, channel in enumerate(self.channels):
            channel.state = bool(value & (1 << i))
