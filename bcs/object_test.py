import typing
import unittest

import bcs


class ObjectTest(unittest.TestCase):
    class Object(bcs.Object):
        def __init__(
            self,
            name: str,
            neighbors: frozenset["ObjectTest.Object"] | None = None,
        ) -> None:
            self.name = name
            self.__neighbors: frozenset["ObjectTest.Object"] = neighbors or frozenset()
            super().__init__()

        def __repr__(self) -> str:
            return self.name

        @property
        def neighbors(self) -> frozenset["ObjectTest.Object"]:
            return self._neighbors

        @property
        def _neighbors(self) -> frozenset["ObjectTest.Object"]:
            return self.__neighbors

        @_neighbors.setter
        def _neighbors(self, _neighbors: frozenset["ObjectTest.Object"]) -> None:
            self._connected_objects = self.__neighbors = _neighbors

        @typing.override
        def validate(self) -> None:
            for neighbor in self.__neighbors:
                if self not in neighbor.__neighbors:
                    raise self.ValidationError(f"{self} not in neighbor {neighbor}")
            super().validate()

        def connect(self, neighbor: "ObjectTest.Object") -> None:
            if neighbor not in self.__neighbors:
                with self._pause_validation():
                    self._neighbors |= {neighbor}
                    neighbor.connect(self)

        def disconnect(self, neighbor: "ObjectTest.Object") -> None:
            if neighbor in self.__neighbors:
                with self._pause_validation():
                    self._neighbors -= {neighbor}
                    neighbor.disconnect(self)

    def test_empty(self) -> None:
        self.Object("a")

    def test_invalid_disconnected_neighbor(self) -> None:
        with self.assertRaises(self.Object.ValidationError):
            self.Object("a", frozenset({self.Object("b")})).validate()

    def test_connect(self) -> None:
        a = self.Object("a")
        b = self.Object("b")
        a.connect(b)
        self.assertSetEqual(a.neighbors, {b})
        self.assertSetEqual(b.neighbors, {a})
        self.assertSetEqual(a.all_connected_objects, {a, b})
        self.assertSetEqual(b.all_connected_objects, {a, b})

    def test_connect_multiple(self) -> None:
        a = self.Object("a")
        b = self.Object("b")
        c = self.Object("c")
        a.connect(b)
        b.connect(c)
        self.assertSetEqual(a.neighbors, {b})
        self.assertSetEqual(b.neighbors, {a, c})
        self.assertSetEqual(c.neighbors, {b})
        self.assertSetEqual(a.all_connected_objects, {a, b, c})
        self.assertSetEqual(b.all_connected_objects, {a, b, c})
        self.assertSetEqual(c.all_connected_objects, {a, b, c})

    def test_disconnect(self) -> None:
        a = self.Object("a")
        b = self.Object("b")
        a.connect(b)
        self.assertSetEqual(a.neighbors, {b})
        self.assertSetEqual(b.neighbors, {a})
        self.assertSetEqual(a.all_connected_objects, {a, b})
        self.assertSetEqual(b.all_connected_objects, {a, b})

        a.disconnect(b)
        self.assertSetEqual(a.neighbors, frozenset())
        self.assertSetEqual(b.neighbors, frozenset())
        self.assertSetEqual(a.all_connected_objects, {a})
        self.assertSetEqual(b.all_connected_objects, {b})
