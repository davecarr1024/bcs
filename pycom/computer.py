import typing
from . import component


class Computer:
    class Error(Exception): ...

    class UnknownComponentError(Error, KeyError): ...

    def __init__(self, *components: component.Component) -> None:
        self.components = frozenset(components)

    @property
    def components(self) -> frozenset[component.Component]:
        return self._components

    @components.setter
    def components(self, components: frozenset[component.Component]) -> None:
        self._components = components

    @property
    def components_by_name(self) -> dict[str, "component.Component"]:
        return {component.name: component for component in self.components}

    def component(self, name: str) -> "component.Component":
        components_by_name = self.components_by_name
        if name not in components_by_name:
            raise self.UnknownComponentError(name)
        return components_by_name[name]

    def apply(
        self,
        action: typing.Union[
            typing.Sequence["component.Component.Action"],
            "component.Component.Action",
        ],
    ) -> None:
        match action:
            case [*_]:
                for action in action:
                    self.apply(action)
            case component.Component.Action():
                self.component(action.component_name).apply(action)

    def update(self) -> None:
        for component in self.components:
            component.update()
