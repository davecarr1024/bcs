import abc
import dataclasses
import typing


@dataclasses.dataclass(kw_only=True)
class Object(abc.ABC):
    class RunTimeout(Exception): ...

    class ValidationError(Exception): ...

    def __post_init__(self) -> None:
        self.validate_all()

    def validate(self) -> None:
        for object in self.connected_objects:
            if self not in object.connected_objects:
                raise self.ValidationError(f"{self} not connected to neighbor {object}")

    @property
    @abc.abstractmethod
    def connected_objects(self) -> typing.Iterable["Object"]: ...

    @property
    @typing.final
    def all_connected_objects(self) -> typing.Iterable["Object"]:
        objects: typing.MutableSequence[Object] = [self]
        pending_objects: typing.MutableSequence[Object] = list(self.connected_objects)
        while pending_objects:
            object = pending_objects.pop()
            if object not in objects:
                objects.append(object)
                pending_objects.extend(object.connected_objects)
        return objects

    @abc.abstractmethod
    def tick(self, t: float, dt: float) -> None: ...

    @property
    @abc.abstractmethod
    def is_stable(self) -> bool: ...

    def apply_to_all(self, f: typing.Callable[["Object"], None]) -> None:
        for object in self.all_connected_objects:
            f(object)

    def validate_all(self) -> None:
        self.apply_to_all(lambda object: object.validate())

    def tick_all(self, t: float, dt: float) -> None:
        self.apply_to_all(lambda object: object.tick(t, dt))

    def run_until(
        self,
        cond: typing.Callable[[], bool],
        *,
        max_t: float = 10,
        dt: float = 0.01,
    ) -> float:
        self.validate_all()
        t: float = 0
        while t < max_t:
            if cond():
                return t
            self.tick_all(t, dt)
            t += dt
        raise self.RunTimeout(f"{self} failed to satisfy condition {cond} in {max_t}s")

    def run_until_stable(
        self,
        *,
        max_t: float = 10,
        dt: float = 0.01,
    ) -> float:
        try:

            def is_stable():
                return self.is_stable

            return self.run_until(is_stable, max_t=max_t, dt=dt)
        except self.RunTimeout:
            raise self.RunTimeout(f"{self} failed to become stable in {max_t}s")
