import contextlib
import typing


class Component:
    class Error(Exception): ...

    class ValidationError(Error): ...

    class ChildNotFoundError(Error, KeyError): ...

    class ControlNotFoundError(Error, KeyError): ...

    def __init__(
        self,
        name: str,
        *,
        parent: typing.Optional["Component"] = None,
        children: typing.Optional[frozenset["Component"]] = None,
        controls: typing.Optional[frozenset["control.Control"]] = None,
    ) -> None:
        self.__name = name
        self.__parent = None
        self.__children: frozenset[Component] = frozenset()
        self.__controls: frozenset["control.Control"] = frozenset()
        self.__pause_validation_count = 0
        with self._pause_validation():
            if parent is not None:
                self.parent = parent
            if children is not None:
                for child in children:
                    self.add_child(child)
            if controls is not None:
                for control in controls:
                    self.add_control(control)

    def __eq__(self, rhs: object) -> bool:
        return self is rhs

    def __hash__(self) -> int:
        return id(self)

    @contextlib.contextmanager
    def _pause_validation(self) -> typing.Iterator[None]:
        try:
            self.__pause_validation_count += 1
            yield
        finally:
            self.__pause_validation_count -= 1
            self._validate_if_enabled()

    @property
    def _validation_enabled(self) -> bool:
        return self.__pause_validation_count == 0

    def _validate_if_enabled(self) -> None:
        if self._validation_enabled:
            self.validate()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def root(self) -> "Component":
        return self.parent.root if self.parent is not None else self

    @property
    def path(self) -> str:
        return (
            f"{self.parent.path}.{self.name}" if self.parent is not None else self.name
        )

    @property
    def parent(self) -> typing.Optional["Component"]:
        return self.__parent

    @parent.setter
    def parent(self, parent: typing.Optional["Component"]) -> None:
        if parent is not self.__parent:
            with self._pause_validation():
                if self.__parent is not None:
                    self.__parent.remove_child(self)
                self.__parent = parent
                if self.__parent is not None:
                    self.__parent.add_child(self)

    @property
    def children(self) -> frozenset["Component"]:
        return self.__children

    def add_child(self, child: "Component") -> None:
        if child not in self.__children:
            self.__children |= frozenset({child})
            child.parent = self

    def remove_child(self, child: "Component") -> None:
        if child in self.__children:
            self.__children -= frozenset({child})
            child.parent = None

    @property
    def children_by_name(self) -> typing.Mapping[str, "Component"]:
        return {child.name: child for child in self.children}

    def child(self, name: str) -> "Component":
        match (dot_pos := name.find(".")):
            case -1:
                if name not in self.children_by_name:
                    raise self.ChildNotFoundError(f"unknown child {name}")
                return self.children_by_name[name]
            case _:
                return self.child(name[:dot_pos]).child(name[dot_pos + 1 :])

    @property
    def controls(self) -> frozenset["control.Control"]:
        return self.__controls

    @property
    def all_controls(self) -> frozenset["control.Control"]:
        controls: set[control.Control] = set(self.controls)
        for child in self.children:
            controls |= child.all_controls
        return frozenset(controls)

    def set_control(self, name: str, value: bool) -> None:
        self.control(name).value = value

    def set_controls(self, *names: str) -> None:
        all_values: dict["control.Control", bool] = {
            control: False for control in self.all_controls
        }
        for name in names:
            all_values[self.control(name)] = True
        for control, value in all_values.items():
            control.value = value

    @property
    def controls_by_name(self) -> typing.Mapping[str, "control.Control"]:
        return {control.name: control for control in self.controls}

    def control(self, name: str) -> "control.Control":
        match (dot_pos := name.find(".")):
            case -1:
                if name not in self.controls_by_name:
                    raise self.ControlNotFoundError(f"unknown control {name}")
                return self.controls_by_name[name]
            case _:
                return self.child(name[:dot_pos]).control(name[dot_pos + 1 :])

    def add_control(self, control: "control.Control") -> None:
        if control not in self.controls:
            with self._pause_validation():
                self.__controls |= frozenset({control})
                control.component = self

    def remove_control(self, control: "control.Control") -> None:
        if control in self.controls:
            with self._pause_validation():
                self.__controls -= frozenset({control})
                control.component = None

    def validate(self) -> None:
        if len(self.children_by_name) != len(self.children):
            raise self.ValidationError(f"duplicate child names")
        for child in self.children:
            if child.parent is not self:
                raise self.ValidationError(
                    f"child {child} not in parent component {self}"
                )
        if self.parent is not None and self not in self.parent.children:
            raise self.ValidationError(f"component {self} not in parent {self.parent}")
        if len(self.controls_by_name) != len(self.controls):
            raise self.ValidationError(f"duplicate control names")
        for control in self.controls:
            if self is not control.component:
                raise self.ValidationError(f"control {control} not in component {self}")
            control.validate()
        for child in self.children:
            child.validate()

    def update(self) -> None:
        for child in self.children:
            child.update()


from . import control
