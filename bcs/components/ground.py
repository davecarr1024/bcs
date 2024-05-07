import typing
from . import component


class Ground(component.Component):
    def __post_init__(self) -> None:
        self._o = self.add_connector("o")
        super().__post_init__()

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._o.state = False
