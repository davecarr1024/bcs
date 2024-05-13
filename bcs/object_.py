import contextlib
import typing


class Object:
    class Error(Exception): ...

    class ValidationError(Error): ...

    def __init__(self) -> None:
        self.__connected_objects: frozenset[Object] = frozenset()
        self.__all_connected_objects: frozenset[Object] | None = frozenset({self})
        self.__pause_validation_count = 0

    def __eq__(self, rhs: object) -> bool:
        return self is rhs

    def __hash__(self) -> int:
        return id(self)

    @property
    def _connected_objects(self) -> frozenset["Object"]:
        return self.__connected_objects

    @_connected_objects.setter
    @typing.final
    def _connected_objects(self, _connected_objects: frozenset["Object"]) -> None:
        self.__connected_objects = _connected_objects
        if self.__all_connected_objects is not None:
            for object in self.__all_connected_objects:
                object.__all_connected_objects = None
        self.validate_all()

    @property
    @typing.final
    def all_connected_objects(self) -> frozenset["Object"]:
        if self.__all_connected_objects is None:
            traversed: set[Object] = set()
            pending: set[Object] = {self}
            while pending:
                object = pending.pop()
                if object not in traversed:
                    traversed.add(object)
                    pending |= object._connected_objects
            self.__all_connected_objects = frozenset(traversed)
        return self.__all_connected_objects

    def validate(self) -> None:
        if self not in self.all_connected_objects:
            raise self.ValidationError(f"{self} not in its own all_connected_objects")
        for object in self._connected_objects:
            if self not in object._connected_objects:
                raise self.ValidationError(f"{self} not in connected object {object}")

    @typing.final
    def validate_all(self) -> None:
        if self.__validation_is_enabled:
            for object in self.all_connected_objects:
                object.__validate_if_enabled()

    def __validate_if_enabled(self) -> None:
        if self.__validation_is_enabled:
            self.validate()

    @property
    def __validation_is_enabled(self) -> bool:
        return self.__pause_validation_count == 0

    @contextlib.contextmanager
    @typing.final
    def _pause_validation(self) -> typing.Iterator[None]:
        self.__pause_validation_count += 1
        try:
            yield
        finally:
            self.__pause_validation_count -= 1
            self.validate_all()
