from . import component


class _Ground(component.Component):
    def __init__(self) -> None:
        super().__init__("ground")
        self.output = self.add_pin("output")

    def update(self) -> None:
        self.output.state = False


ground_ = _Ground()
