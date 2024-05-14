import contextlib
import typing
from .. import component


class Clock(component.Component):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)
        self.enable = self.add_pin("enable")
        self.output = self.add_pin("output")
        self.__pause_update_count = 0

    @contextlib.contextmanager
    def _pause_update(self) -> typing.Iterator[None]:
        try:
            self.__pause_update_count += 1
            yield
        finally:
            self.__pause_update_count -= 1

    @property
    def _update_enabled(self) -> bool:
        return self.__pause_update_count == 0

    @typing.override
    def update(self) -> None:
        super().update()
        if self.enable.state and self._update_enabled:
            with self._pause_update():
                self.output.state = not self.output.state

    def pulse(self) -> None:
        with self._pause_update():
            self.output.state = False
            self.output.state = True
            self.output.state = False
