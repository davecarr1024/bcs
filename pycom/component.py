import abc
import dataclasses
import typing

_Component = typing.TypeVar("_Component", bound="Component")


class Component:
    class Error(Exception): ...

    @dataclasses.dataclass(frozen=True)
    class UnknownActionError(Error):
        component: "Component"
        action: "Component.Action"

    @dataclasses.dataclass(frozen=True)
    class Action(abc.ABC, typing.Generic[_Component]):
        component_name: str

        @abc.abstractmethod
        def __call__(self, component: _Component) -> None: ...

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def apply(self, action: Action) -> None:
        raise self.UnknownActionError(self, action)

    def update(self) -> None: ...