from . import component


class _Power(component.Component):
    def __init__(self) -> None:
        super().__init__("power")
        self.output = self.add_pin("output")

    def update(self) -> None:
        self.output.state = True


power_ = _Power()
