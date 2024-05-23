import typing


class Signal:
    def __init__(
        self,
        name: str,
        component: typing.Optional["component_lib.Component"] = None,
    ) -> None:
        self._name = name
        self._component = None
        if component is not None:
            self.component = component


from . import component as component_lib
