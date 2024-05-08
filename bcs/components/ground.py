import typing
from . import component


class Ground(component.Component):
    def __post_init__(self) -> None:
        super().__post_init__()
        self._o = self.add_connector("o")

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._o.state = False
