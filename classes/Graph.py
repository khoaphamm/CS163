import heapq
from collections import defaultdict 
from math import sqrt
from helper.compute import convert_lnglat_to_xy


TIME_CONSTANT = 0.2111032115910458

class Graph:

    def __init__(self):
        self.adjacency_list = defaultdict(list)
        self.distances = [float('inf')] * 10000
        self.predecessors = [-1] * 10000
        self.route_data = [tuple()] * 10000
        self.path_data = [list()] * 10000
        self.stops_data = [{}] * 10000
        self.position = [()] * 10000

    def add_edge(self, node_u, node_v, weight):
        self.adjacency_list[node_u].append((node_v, weight))

    def set_node(self, node_u, stop_data):
        X, Y = convert_lnglat_to_xy(stop_data["Lng"], stop_data["Lat"])
        self.stops_data[node_u] = stop_data
        self.position[node_u] = (X, Y)

    def reset_graph(self):
        self.distances = [float('inf')] * 10000
        self.predecessors = [-1] * 10000
        self.route_data = [tuple()] * 10000
        self.path_data = [list()] * 10000


    def heuristic(self, node, destination):
        node_x, node_y = self.position[node]
        dest_x, dest_y = self.position[destination]
        if None in {node_x, node_y, dest_x, dest_y}:
            return 0.0
        return sqrt(((node_x - dest_x) ** 2 + (node_y - dest_y) ** 2)) * TIME_CONSTANT


    def update_edge(self, node_u, node_v, weight):
        neighbor = node_v
        current_node = node_u
        current_distance = self.distances[current_node]
        distance = weight[0] #0 for time, #1 for distance
        route = (weight[2], weight[3])
        lng_path, lat_path = weight[4], weight[5]
                
        self.distances[neighbor] = current_distance + distance
        self.route_data[neighbor] = route
        self.path_data[neighbor] = (lng_path, lat_path)
        self.predecessors[neighbor] = current_node


    def one_source_dijkstra(self, source):
        priority_queue = []
        heapq.heappush(priority_queue, (0, source))
        self.distances[source] = 0
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            for neighbor, weight in self.adjacency_list[current_node]:
                distance = weight[0]  # 0 for time, 1 for distance
                if current_distance + distance < self.distances[neighbor]:
                    self.update_edge(current_node, neighbor, weight)
                    heapq.heappush(priority_queue, (self.distances[neighbor], neighbor))


    def dijkstra(self, source, destination):
        priority_queue = []
        visited_stops = set()
        heapq.heappush(priority_queue, (0, source))
        # visited_stops.add(source)
        self.distances[source] = 0
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            # visited_stops.add(current_node)
            if current_node == destination:  # Stop if the destination is reached
                break
            for neighbor, weight in self.adjacency_list[current_node]:
                distance = weight[0]  # 0 for time, 1 for distance
                if  current_distance + distance < self.distances[neighbor]:
                    self.update_edge(current_node, neighbor, weight)
                    heapq.heappush(priority_queue, (self.distances[neighbor], neighbor))
        
        return list(visited_stops)

    

    def astar(self, source, destination):
        priority_queue = []
        visited_stops = set()
        heapq.heappush(priority_queue, (0 + self.heuristic(source, destination), 0, source))
        # visited_stops.add(source)
        self.distances[source] = 0

        while priority_queue:
            estimated_cost, current_distance, current_node = heapq.heappop(priority_queue)
            # visited_stops.add(current_node)


            if current_node == destination:  # Stop if the destination is reached
                break

            for neighbor, weight in self.adjacency_list[current_node]:
                distance = weight[0]  # 0 for time, 1 for distance
                if self.distances[neighbor] > current_distance + distance:
                    self.update_edge(current_node, neighbor, weight)
                    heapq.heappush(priority_queue, (self.distances[neighbor] + self.heuristic(neighbor, destination), self.distances[neighbor], neighbor))
                    

        return list(visited_stops)  # Convert set to list if needed