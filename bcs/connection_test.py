import unittest

from bcs import connection
import bcs


class ConnectionTest(unittest.TestCase):
    def test_connect_power(self) -> None:
        a = connection.Connection()
        a.connect_power()
        a.run_until_stable_with_state(True)

    def test_connect_connections(self) -> None:
        a = connection.Connection()
        b = connection.Connection()
        a.connect(b)
        a.connect_power()
        b.run_until_stable_with_state(True)

    def test_not(self) -> None:
        for a, o in list[tuple[bool, bool]](
            [
                (False, True),
                (True, False),
            ]
        ):
            with self.subTest(a=a, o=o):
                c = bcs.components.Component()
                ac = c.add_connector("a")
                oc = c.add_connector("o")
                oc.connect(~ac)
                ac.state = a
                oc.run_until_stable_with_state(o)

    def test_and(self) -> None:
        for a, b, o in list[tuple[bool, bool, bool]](
            [
                (False, False, False),
                (False, True, False),
                (True, False, False),
                (True, True, True),
            ]
        ):
            with self.subTest(a=a, b=b, o=o):
                c = bcs.components.Component()
                ac = c.add_connector("a")
                bc = c.add_connector("b")
                oc = c.add_connector("o")
                oc.connect(ac & bc)
                ac.state = a
                bc.state = b
                oc.run_until_stable_with_state(o)

    def test_or(self) -> None:
        for a, b, o in list[tuple[bool, bool, bool]](
            [
                (False, False, False),
                (False, True, True),
                (True, False, True),
                (True, True, True),
            ]
        ):
            with self.subTest(a=a, b=b, o=o):
                c = bcs.components.Component()
                ac = c.add_connector("a")
                bc = c.add_connector("b")
                oc = c.add_connector("o")
                oc.connect(ac | bc)
                ac.state = a
                bc.state = b
                oc.run_until_stable_with_state(o)

    def test_xor(self) -> None:
        for a, b, o in list[tuple[bool, bool, bool]](
            [
                (False, False, False),
                (False, True, True),
                (True, False, True),
                (True, True, False),
            ]
        ):
            with self.subTest(a=a, b=b, o=o):
                c = bcs.components.Component()
                ac = c.add_connector("a")
                bc = c.add_connector("b")
                oc = c.add_connector("o")
                oc.connect(ac ^ bc)
                ac.state = a
                bc.state = b
                oc.run_until_stable_with_state(o)
