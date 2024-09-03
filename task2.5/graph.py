from Classes.Graph import Graph
from helper.converter import *

g = Graph()

filename1 = 'data/type12.csv'
filename2 = 'data/type34.csv'

GMTp7 = 7

all_stops = set()

cnt = 0


def buildGraph(filename, type):
    global cnt
    file = open(filename, "r")

    for line in file:
        data = line.strip().split(',')

        # structure of CSV file:
        # stop_id1,route_id1,var_id1,timestamp1,stop_id2,route_id2,var_id2,timestamp2,
        # time_diff,latx1,lngy1,latx2,lngy2,vehicle_number1,vehicle_number2,
        # node_type1,node_type2,node_pos1,node_pos2,edge_pos,edge_type

        node_u = int(data[0])
        node_v = int(data[4])

        if node_u == node_v:
            continue

        all_stops.add(node_u)
        all_stops.add(node_v)

        epoch_time_start = int(float(data[3]))
        epoch_time_end = int(float(data[7]))

        second_in_day_start = convertToDatetime(epoch_time_start, GMTp7)
        second_in_day_end = convertToDatetime(epoch_time_end, GMTp7)

        time_diff = epoch_time_end - epoch_time_start

        #weight format (number of transit, start time, time diff)

        weight = (0, second_in_day_start, time_diff)

        if type == "34":
            weight = (1, second_in_day_start, time_diff)

        g.add_edge(node_u, node_v, weight)
        cnt += 1
        if cnt % 50000 == 0:
            print(cnt)
    
def allPairsShortestPath():
    total = len(all_stops)
    count = 0
    for stop in all_stops:
        g.reset_graph()
        g.one_source_dijkstra(stop)
        count += 1
        g.update_importance(stop, all_stops)
        print("Progress: " + str(count) + "/" + str(total))

def saveToFile(importance_stops):
    file = open("output.txt", "w")
    for stop in importance_stops:
        file.write(str(stop) + " " + str(g.importance[stop]) + "\n")
    file.close()

        

buildGraph(filename1, "12")
buildGraph(filename2, "34")

print("Graph built successfully")
all_stops = list(all_stops)

print(len(all_stops))

for stop in all_stops:
    for adj_stop in g.adjacency_list[stop]:
        weights = g.adjacency_list[stop][adj_stop]
        g.adjacency_list[stop][adj_stop] = sorted(weights, key=lambda x: x[1])

print("Weights sorted successfully")

allPairsShortestPath()

print("All pairs shortest path computed successfully")

stop_list = g.find_k_most_important_stops(10)

for stop in stop_list:
    print(stop, g.importance[stop])

print("Top 10 most important stops computed successfully")

saveToFile(stop_list)
