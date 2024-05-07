import abc
import dataclasses
import typing


@dataclasses.dataclass(kw_only=True)
class Object(abc.ABC):
    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        assert all(
            self in object.connected_objects for object in self.connected_objects
        )

    @property
    @abc.abstractmethod
    def connected_objects(self) -> typing.Iterable["Object"]:
        ...

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
    def tick(self, t: float, dt: float) -> None:
        ...

    @property
    @abc.abstractmethod
    def is_stable(self) -> bool:
        ...

    def apply_to_all(self, f: typing.Callable[["Object"], None]) -> None:
        print(f"apply_to_all {len(list(self.all_connected_objects))}")
        for object in self.all_connected_objects:
            f(object)

    def validate_all(self) -> None:
        self.apply_to_all(lambda object: object.validate())

    def tick_all(self, t: float, dt: float) -> None:
        self.apply_to_all(lambda object: object.tick(t, dt))

    def run_until_stable(self, *, max_t: float = 10, dt: float = 0.01) -> float:
        self.validate_all()
        t: float = 0
        print(f"run_until_stable {max_t} {dt}")
        while t < max_t:
            print(f"tick {dt} {t}/{max_t}")
            self.tick_all(t, dt)
            t += dt
            if self.is_stable:
                print(f"stable - quitting")
                return t
        raise Exception(f"failed to become stable in {max_t}")
