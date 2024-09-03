import osmium

class OSMGraph(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.node_ways = {}
        self.node_locations = {}
        self.edges = {}

    def node(self, n):
        self.node_ways[n.id] = []
        self.node_locations[n.id] = (n.location.lon, n.location.lat)

    def way(self, w):
        nodes = list(w.nodes)  # Store nodes in a list to prevent runtime issues
        for i in range(len(nodes) - 1):
            node1 = nodes[i].ref
            node2 = nodes[i + 1].ref
            self.edges[(node1, node2)] = w.id
    
    def retrieve_edge(self, node1, node2):
        return self.edges.get((node1, node2), None)

        