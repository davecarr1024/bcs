import typing
from pycom.components import component, control


class Clock(component.Component):
    def __init__(
        self,
        name: typing.Optional[str] = None,
    ) -> None:
        self.__disable = control.Control("disable")
        super().__init__(
            name or "clock",
            controls=[
                self.__disable,
            ],
        )

    @property
    def disable(self) -> bool:
        return self.__disable.value

    @disable.setter
    def disable(self, disable: bool) -> None:
        self.__disable.value = disable

    def run(self) -> int:
        num_updates: int = 0
        self.disable = False
        while not self.disable:
            self.root.tick()
            num_updates += 1
        return num_updates
