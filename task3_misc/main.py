import osmium
import networkx as nx
import random
import pickle
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import json


# Function to get a subgraph with a random sample of nodes
def get_subgraph(G, sample_size):
    sampled_nodes = random.sample(list(G.nodes()), sample_size)
    return G.subgraph(sampled_nodes)

class IntersectionHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.node_ways = {}
        self.ways = []
        self.node_locations = {}

    def node(self, n):
        self.node_ways[n.id] = []
        self.node_locations[n.id] = (n.location.lon, n.location.lat)

    def way(self, w):
        nodes = list(w.nodes)  # Store nodes in a list to prevent runtime issues
        for n in nodes:
            if n.ref in self.node_ways:
                self.node_ways[n.ref].append(w.id)
        self.ways.append((w.id, nodes))

# Initialize the handler and apply it to the OSM file
handler = IntersectionHandler()
handler.apply_file("E:\\DIN\\Note-taking-2023\\CS163_LAB\\BUSMAP\\CS163\\task3_misc\\highways.osm")

real_edges = {}

# Identify intersections
intersections = {node_id for node_id, ways in handler.node_ways.items() if len(ways) > 1}

# Create the graph
G = nx.Graph()

# Add nodes (intersections)
for intersection in intersections:
    G.add_node(intersection, pos=handler.node_locations[intersection])

# Add edges (ways between intersections)
for way_id, way_nodes in handler.ways:
    valid_nodes = []
    node_to_position = {}

    for i, node in enumerate(way_nodes):
        if node.ref in intersections and node.ref in handler.node_locations:
            valid_nodes.append(node.ref)
            node_to_position[node.ref] = i

    if len(valid_nodes) >= 2:
        for i in range(len(valid_nodes) - 1):
            u = valid_nodes[i]
            v = valid_nodes[i + 1]

            if(u == v): continue

            start = node_to_position[u]
            end = node_to_position[v] + 1

            for i in range(start, end):
                node1 = way_nodes[i].ref
                node2 = way_nodes[i + 1].ref
                real_edges[(node1, node2)] = (u, v)
            
            # Store the subpath in the edge attributes
            G.add_edge(u, v)


print(f"Number of nodes (intersections): {G.number_of_nodes()}")
print(f"Number of edges (ways): {G.number_of_edges()}")

# # Find communities in the graph
# communities = greedy_modularity_communities(G)

# # Assign colors to each community
# color_map = {}
# for i, community in enumerate(communities):
#     for node in community:
#         color_map[node] = i

# # Get positions for the nodes
# pos = nx.get_node_attributes(G, 'pos')

# # Draw the graph with community colors
# plt.figure(figsize=(12, 8))
# nx.draw(G, pos, node_size=1 , node_color=[color_map[node] for node in G.nodes()], with_labels=False, edge_color='gray', cmap=plt.cm.rainbow, alpha=0.5)
# plt.title("Graph of Intersections and Ways in Ho Chi Minh City with Communities")
# plt.show()
