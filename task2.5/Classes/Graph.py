import heapq
from collections import defaultdict 
from helper.converter import *

class Graph:

    def __init__(self):
        self.adjacency_list = defaultdict(lambda: defaultdict(list))
        self.distances = [float('inf')] * 10000
        self.predecessors = [-1] * 10000
        self.importance = [0] * 10000
        self.start_time = [1000000] * 10000

    def add_edge(self, node_u, node_v, weight):
        self.adjacency_list[node_u][node_v].append(weight)

    def reset_graph(self):
        self.distances = [float('inf')] * 10000
        self.predecessors = [-1] * 10000
        self.start_time = [1000000] * 10000


    def update_edge(self, node_u, node_v, weight):
        neighbor = node_v
        current_node = node_u
        current_distance = self.distances[current_node]
        distance = weight[0] 
 
        self.start_time[neighbor] = min(self.start_time[neighbor], weight[1] + weight[2])
                
        self.distances[neighbor] = current_distance + distance
        self.predecessors[neighbor] = current_node


    def one_source_dijkstra(self, source):
        priority_queue = []
        heapq.heappush(priority_queue, (0, source))
        self.distances[source] = 0
        self.start_time[source] = 0
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            for neighbor in self.adjacency_list[current_node]:
                weights = self.adjacency_list[current_node][neighbor]
                cur_time = self.start_time[current_node]
                weight = smallest_larger_than_x(weights, cur_time) 
                if weight is None:
                    continue 
                distance = weight[0]  # 0 for transit, 1 for time, 2 for time diff
                if current_distance + distance < self.distances[neighbor]:
                    self.update_edge(current_node, neighbor, weight)
                    heapq.heappush(priority_queue, (self.distances[neighbor], neighbor))
                
    def find_k_most_important_stops(self, k):
        # Find the k largest values in the list
        k_largest_values = heapq.nlargest(k, self.importance)
        
        # Find the indexes of these values in the original list
        k_largest_indexes = [i for i, value in enumerate(self.importance) if value in k_largest_values]
        
        # If there are duplicates, ensure we only get k indexes
        return k_largest_indexes[:k]

    def update_importance(self, source, stops):
        # Update the importance of each stop
        for stop in stops:
            cur_stop = stop
            if self.predecessors[cur_stop] == -1:
                continue    
            while cur_stop != source:
                self.importance[cur_stop] += 1
                cur_stop = self.predecessors[cur_stop]