from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.aiohttp.transport import AiohttpTransport
from gremlin_python.process.traversal import *

import os

port = 8182
server = "(your server endpoint)"

endpoint = f"wss://{server}:{port}/gremlin"

graph = Graph()

connection = DriverRemoteConnection(
    endpoint, "g", transport_factory=lambda: AiohttpTransport(call_from_event_loop=True)
)

g = graph.traversal().withRemote(connection)

results = (
    g.V()
    .hasLabel("airport")
    .sample(10)
    .order()
    .by("code")
    .local(__.values("code", "city").fold())
    .toList()
)

# Print the results in a tabular form with a row index
for i, c in enumerate(results, 1):
    print("%3d %4s %s" % (i, c[0], c[1]))

connection.close()
