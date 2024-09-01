import osmium
import networkx as nx
import random
import pickle
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import json
import os
from helper.fileReader import dataReader, dataWriter
from osm_helper import OSMGraph


INPUT_FILE_PATH = os.path.abspath("data/{}")
INPUT_FILENAME = "highways.osm"
real_edges = {}

# Initialize the handler and apply it to the OSM file

graph = OSMGraph()
graph.apply_file(INPUT_FILE_PATH.format(INPUT_FILENAME))


# Create the graph
G = nx.Graph()

# Add nodes 
for node_id, node_location in graph.node_locations.items():
    G.add_node(node_id, pos=node_location)

# Add edges
for edge, way_id in graph.edges.items():
    u, v = edge
    G.add_edge(u, v, way_id=way_id)
    real_edges[(u, v)] = (u, v, way_id)


print(f"Number of nodes (intersections): {G.number_of_nodes()}")
print(f"Number of edges (ways): {G.number_of_edges()}")

print(len(real_edges))

# ####################
# # draw the graph

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
# ####################

data, filename = dataReader("bus-history.json")
H = nx.Graph()

test_bus_path = data[1]["tripList"][5]["edgesOfPath2"]
test_bus_edges = []
test_bus_nodes = set()

all_trips = []
trace_trips = {} # map fron bus_edge to list of bus trips that use that edge
edges_matrix = {}
cnt = 0

cnt_failed = 0
cnt_pros = 0

for bus in data:
    for trip in bus["tripList"]:
        bus_path = trip["edgesOfPath2"]

        for i in range(len(bus_path) - 1):
        #for i in range(min(1, len(bus_path) - 1)):
            for j in range(i+1, len(bus_path) - 1):
            #for j in range(i+1, min(i+2, len(bus_path))):
                u1 = int(bus_path[i][0])
                v1 = int(bus_path[i][1])
                u2 = int(bus_path[j][0])
                v2 = int(bus_path[j][1])

                edge1 = real_edges.get((u1, v1), None)
                edge2 = real_edges.get((u2, v2), None)
                
                if edge1 is not None and edge2 is not None and edge1 != edge2:
                    
                    save_edge = None
                    for k in range(i + 1, j - 1):
                        u = int(bus_path[k][0])
                        v = int(bus_path[k][1])
                        key = f"{edge1}-{edge2}"
                        edge_id = real_edges.get((u, v), None)
                        if edge_id is not None and edge_id != save_edge:
                            if key not in edges_matrix and len(edges_matrix) < 1327214:
                                edges_matrix[key] = {}
                            cnt_trips = edges_matrix.get(key, {}).get(edge_id, 0)
                            if(key not in edges_matrix):
                                continue
                            edges_matrix[key][edge_id] = cnt_trips + 1
                            save_edge = edge_id
                    

                

            
        cnt += 1
        print(f"Processed {cnt} trips")
        print(f"cur_process: {len(edges_matrix)}")


result = {}

for edge_pair in edges_matrix:
    most_freq = max(edges_matrix[edge_pair].values())
    for edge_id, cnt_trips in edges_matrix[edge_pair].items():
        if (cnt_trips == most_freq):
            result[edge_pair] = (edge_id, cnt_trips) 

filename = "edges_matrix.txt"

with open(filename, 'w', encoding='utf-8') as f:
        for key, value in result.items():
            edge = value[0][2]
            cnt_trips = value[1]
            f.write(str(key) + ': ' + str(edge) + ', ' + str(cnt_trips) + '\n')

print(f"edges_matrix written to {filename}")


# print(len(all_trips))

# filename = dataWriter(all_trips, "bus_edges_test.json")

# print(f"bus_edges written to {filename}")

# filename = dataWriter(trace_trips, "trace_trips2_test.json")

# print(f"trace_trips written to {filename}")

 

