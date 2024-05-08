import unittest

import bcs


class ConnectorTest(unittest.TestCase):
    def test_create_connector(self) -> None:
        c = bcs.components.Component()
        a = bcs.Connector(name="a", component=c)
        self.assertIs(a.component, c)
        self.assertIn(a, c.connectors)

    def test_connect_connector(self) -> None:
        c = bcs.components.Component()
        a = bcs.Connector(name="a", component=c)
        b = bcs.Connector(name="b", component=c)
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        b.run_until_stable_with_state(True)
        self.assertTrue(b.state)

    def test_connect_connection(self) -> None:
        connector = bcs.Connector(
            name="a",
            component=bcs.components.Component(),
        )
        connection = bcs.Connection()
        connector.connect(connection)
        self.assertCountEqual(connection.connectors, [connector])
        self.assertCountEqual(connector.connections, [connection])

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
