import dataclasses
import typing
import unittest

import bcs


class ObjectTest(unittest.TestCase):
    @dataclasses.dataclass(repr=False)
    class _Object(bcs.Object):
        name: str
        _neighbors: typing.Sequence["ObjectTest._Object"] = dataclasses.field(
            init=False,
            default_factory=list,
            compare=False,
            repr=False,
        )

        def __str__(self) -> str:
            return repr(self)

        def __repr__(self) -> str:
            return (
                f"{self.name}({','.join(neighbor.name for neighbor in self.neighbors)})"
            )

        @typing.override
        def validate(self) -> None:
            if len(self.neighbors) != len(self._connected_objects):
                raise self.ValidationError(
                    f"neighbors {self.neighbors} != connected_objects {self._connected_objects}"
                )
            for neighbor in self.neighbors:
                if self not in neighbor.neighbors:
                    raise self.ValidationError(
                        f"neighbor {neighbor} doesn't contain object {self}"
                    )
            super().validate()

        @typing.override
        def tick(self, t: float, dt: float) -> None: ...

        @property
        @typing.override
        def is_stable(self) -> bool:
            return True

        @property
        def neighbors(self) -> typing.Sequence["ObjectTest._Object"]:
            return self._neighbors

        @neighbors.setter
        def neighbors(self, neighbors: typing.Sequence["ObjectTest._Object"]) -> None:
            self._connected_objects = self._neighbors = neighbors

        def connect(self, neighbor: "ObjectTest._Object") -> None:
            if neighbor not in self._neighbors:
                with self._pause_validation():
                    self.neighbors = list(self.neighbors) + [neighbor]
                    neighbor.connect(self)

    def test_empty(self) -> None:
        a = self._Object("a")
        self.assertCountEqual(a.neighbors, [])
        self.assertCountEqual(a.all_connected_objects, [a])

    def test_neighbor(self) -> None:
        a = self._Object("a")
        b = self._Object("b")
        a.connect(b)
        self.assertCountEqual(a.neighbors, [b])
        self.assertCountEqual(b.neighbors, [a])
        self.assertCountEqual(a.all_connected_objects, [a, b])
        self.assertCountEqual(b.all_connected_objects, [a, b])

    def test_network(self) -> None:
        a = self._Object("a")
        b = self._Object("b")
        c = self._Object("c")
        a.connect(b)
        b.connect(c)
        self.assertCountEqual(a.neighbors, [b])
        self.assertCountEqual(b.neighbors, [a, c])
        self.assertCountEqual(c.neighbors, [b])
        self.assertCountEqual(a.all_connected_objects, [a, b, c])
        self.assertCountEqual(b.all_connected_objects, [a, b, c])
        self.assertCountEqual(c.all_connected_objects, [a, b, c])
