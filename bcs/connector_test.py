import unittest

import bcs


class ConnectorTest(unittest.TestCase):
    def test_invalid_connection(self) -> None:
        with self.assertRaises(BaseException):
            bcs.Connector(
                name="a",
                component=bcs.components.Component(),
                connections=[
                    bcs.Connection(),
                ],
            )

    def test_connect_connection(self) -> None:
        connector = bcs.Connector(
            name="a",
            component=bcs.components.Component(),
        )
        connection = bcs.Connection()
        connector.connect(connection)
        connector.validate()
        connection.validate()
        self.assertIn(connector, connection.connectors)
        self.assertIn(connection, connector.connections)

    def test_connector(self) -> None:
        c = bcs.components.Component()
        a = bcs.Connector(name="a", component=c)
        b = bcs.Connector(name="b", component=c)
        c.validate_all()
        self.assertIn(a, c.connectors)
        self.assertIn(b, c.connectors)

    def test_connection_propagates_state(self) -> None:
        connector = bcs.Connector(
            name="a",
            component=bcs.components.Component(),
        )
        connection = bcs.Connection()
        connector.connect(connection)
        self.assertFalse(connection.state)
        connector.state = True
        connection.run_until_stable_with_state(True)
        self.assertTrue(connection.state)
