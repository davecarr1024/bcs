import typing
from .. import component


class TristateBuffer(component.Component):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)
        self.input = self.add_pin("input")
        self.enable = self.add_pin("enable")
        self.output = self.add_pin("output")

    @typing.override
    def update(self) -> None:
        super().update()
        if self.enable.state:
            self.output.state = self.input.state
