import typing
from .. import component
from ... import pin


class Register(component.Component):
    def __init__(
        self,
        size: int = 0,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)
        self.data_pins: typing.Sequence[pin.Pin] = [
            self.add_pin(f"input_%d" % i) for i in range(size)
        ]
