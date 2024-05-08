import abc
import contextlib
import dataclasses
import typing

MAX_T: float = 10
DT: float = 0.001
_id: int = 0


@dataclasses.dataclass
class Object(abc.ABC):
    class RunTimeout(Exception): ...

    class ValidationError(Exception): ...

    __connected_objects: typing.Sequence["Object"] = dataclasses.field(
        default_factory=list,
        init=False,
        repr=False,
        compare=False,
    )
    __all_connected_objects: typing.Sequence["Object"] = dataclasses.field(
        default_factory=list,
        init=False,
        repr=False,
        compare=False,
    )
    __pause_validation_count: int = dataclasses.field(
        default=0,
        init=False,
        compare=False,
        repr=False,
    )
    id: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        global _id
        self.id = _id
        _id += 1
        self._connected_objects = self.__connected_objects

    @property
    def _connected_objects(self) -> typing.Sequence["Object"]:
        return self.__connected_objects

    @_connected_objects.setter
    def _connected_objects(self, _connected_objects: typing.Sequence["Object"]) -> None:
        self.__connected_objects = _connected_objects
        self.__all_connected_objects = []
        self.__traverse_object_graph(self.__all_connected_objects.append)

        def set_all_connected_objects(object: Object) -> None:
            object.__all_connected_objects = self.__all_connected_objects

        self.apply_to_all(set_all_connected_objects)
        self.validate_all_if_enabled()

    @property
    def all_connected_objects(self) -> typing.Sequence["Object"]:
        return self.__all_connected_objects

    def __traverse_object_graph(
        self,
        f: typing.Callable[["Object"], None],
    ) -> None:
        traversed: typing.MutableSequence[Object] = []
        pending: typing.MutableSequence[Object] = [self]
        while pending:
            object = pending.pop()
            if object not in traversed:
                traversed.append(object)
                pending.extend(object._connected_objects)
                f(object)

    @abc.abstractmethod
    def tick(self, t: float, dt: float) -> None: ...

    @property
    @abc.abstractmethod
    def is_stable(self) -> bool: ...

    def apply_to_all(self, f: typing.Callable[["Object"], None]) -> None:
        for object in self.all_connected_objects:
            f(object)

    def validate_if_enabled(self) -> None:
        if self._is_validation_enabled:
            self.validate()

    def validate(self) -> None:
        for object in self._connected_objects:
            if self not in object._connected_objects:
                raise self.ValidationError(f"{self} not connected to neighbor {object}")

    def validate_all_if_enabled(self) -> None:
        if self._is_validation_enabled:
            self.apply_to_all(lambda object: object.validate_if_enabled())

    @property
    def _is_validation_enabled(self) -> bool:
        return self.__pause_validation_count == 0

    @contextlib.contextmanager
    def _pause_validation(self) -> typing.Iterator[None]:
        self.__pause_validation_count += 1
        try:
            yield
        finally:
            self.__pause_validation_count -= 1
            self.validate_all_if_enabled()

    def tick_all(self, t: float, dt: float) -> None:
        self.apply_to_all(lambda object: object.tick(t, dt))

    def run_until(
        self,
        cond: typing.Callable[[], bool],
        *,
        max_t: float = MAX_T,
        dt: float = DT,
    ) -> float:
        self.validate_all_if_enabled()
        t: float = 0
        while t <= max_t:
            if cond():
                return t
            self.tick_all(t, dt)
            t += dt
        raise self.RunTimeout(f"{self} failed to satisfy condition {cond} in {max_t}s")

    def run_until_stable(
        self,
        *,
        max_t: float = MAX_T,
        dt: float = DT,
    ) -> float:
        try:

            def is_stable():
                return self.is_stable

            return self.run_until(is_stable, max_t=max_t, dt=dt)
        except self.RunTimeout:
            raise self.RunTimeout(f"{self} failed to become stable in {max_t}s")
