from collections import defaultdict
import json
from classes.Graph import *
from stops import getListStop
from vars import getListRoute
from paths import getListPath
from helper.fileReader import dataReader
from classes.Stop import *
from graph import *
import os

INPUT_FILENAME = "stops.json"
OUTPUT_FILENAME_JSON = "new_zone_stops.json"
OUTPUT_FILENAME_PAIR_JSON = "shortest_pair.json"


listRoute = getListRoute()
listStop = getListStop()
listPath = getListPath()
allStop = getAllStop()
g = Graph()   

def getListStop():
    try:
        stopsGroup, filename = dataReader(INPUT_FILENAME)
        
        res = dict()
        
        for stops in stopsGroup:
            if not stops:
                continue
            for stop in stops["Stops"]:
                res[stop["StopId"]] = stop
        
        # Assuming RouteVarQuery processes the list of routes in some way
        listRoutes = ListStops(res)
        return listRoutes

    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return []

def buildThisGraph():

  for data in listStop.allStops:
    #print(type(data), data)

    # Get routeId and routeVarId of stop
    routeId = int(data.RouteId)
    routeVarId = int(data.RouteVarId)
    runningTime = None
    totalDistance = None
    # Get running time and total distance of route
    for routes in listRoute.routeGroup:
      route = routes.routeVar
      if (route["RouteId"] == routeId):
        runningTime = route["RunningTime"]
        totalDistance = route["Distance"]
        break
  
    if not runningTime or not totalDistance:
      continue
    # Get path have same RouteId and RouteVarId
    choosenPath = None
    for paths in listPath.pathGroup:
      if int(paths.RouteId) == routeId and int(paths.RouteVarId) == routeVarId:
        choosenPath = paths
    if not choosenPath:
      continue
    
    # Store all stopId and coordinate of stop
    # for stop in data.Stops: 
      # allStop[stop["StopId"]] = {"Lat": stop["Lat"], "Lng": stop["Lng"], "Name": stop["Name"]}
      

    # Calculate average running time between 2 stops
    runningTime = (runningTime * 60)
    timeBase = runningTime / totalDistance

    # Calculate average distance between 2 stops
    # Add info of stop to graph
    g.setNode(data.Stops[0]["StopId"], data.Stops[0])
    for i in range(len(data.Stops) - 1):
      lngPath = list()
      latPath = list()

      distance = findDistance(choosenPath, lngPath, latPath, data.Stops[i], data.Stops[i + 1]) 
      timeCost = distance * timeBase
      
      # Add edge between 2 stops
      g.addEdge(data.Stops[i]["StopId"], data.Stops[i + 1]["StopId"], (timeCost, distance, routeId, routeVarId, lngPath, latPath))
      # Add info of stop to graph
      g.setNode(data.Stops[i + 1]["StopId"], data.Stops[i + 1])


def getZoneStop():
    zones_data = defaultdict(list)
    
    # Assuming each stop has a .zone attribute and is already a dictionary or can be converted to one
    for stop in allStop.values():
        if not stop:
            continue
        zones_data[stop["Zone"]].append(stop)  # Assuming dict(stop) converts a Stop object to a dictionary

    # Output to JSON
    OUTPUT_FILE_PATH = os.path.abspath("output/{}")
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH.format(OUTPUT_FILENAME_PAIR_JSON)), exist_ok=True)
    with open(OUTPUT_FILE_PATH.format(OUTPUT_FILENAME_PAIR_JSON), 'w', encoding="UTF-8") as file:
        json.dump(zones_data, file, indent=4, ensure_ascii=False)

    print(f"Zones and their stops have been saved to {OUTPUT_FILENAME_PAIR_JSON}.")
    
    return zones_data

def getPairBetweenZoneHelper(src_list, dest_list):
    res = dict()

    
    res["RunningTime"] = 1000000.0

    # for start_stop in src_list:
    #     for end_stop in dest_list:
    #         this_route = shortestPath(start_stop["StopId"], end_stop["StopId"])
    #         if not res or (res["RunningTime"] > this_route["RunningTime"]):
    #             res = this_route
    for start_stop in src_list:
        g.reset()
        g.oneNodeDijkstra(int(start_stop["StopId"]))
        
        for end_stop in dest_list:

            if (res["RunningTime"] > g.dist[int(end_stop["StopId"])]):
                u = int(start_stop["StopId"])
                v = int(end_stop["StopId"])
                res["StartStopId"] = u
                res["EndStopId"] = v
                res["RunningTime"] = g.dist[v]

                stopIds = list()
                while (v != -1 and u != v):
                    stopIds.append(v)
                    v = g.pre[v]
                    if (u == v):
                        stopIds.append(v)
                        break
                stopIds.reverse()
                
                res["StopIds"] = stopIds

                pathRoute = list()
                for stopId in stopIds:
                    if g.routeRef[stopId]: 
                        pathRoute.append({ "lat": g.pathRef[stopId][1], "lng": g.pathRef[stopId][0], "RouteId": g.routeRef[stopId][0], "RouteVarId": g.routeRef[stopId][1]})    

                res["Path"] = pathRoute
            
        

    return res

def getPairBetweenZone():
    zones_data = defaultdict(list)
    zones_data = getZoneStop()

    zone_list = list(zones_data.keys())
    
    allPairZones = dict()

    cnt = 0

    for i in range(len(zone_list)):
        for j in range(len(zone_list)):
            if i == j:
                continue
            print(i, j)
            src = zone_list[i]
            dest = zone_list[j]
            allPairZones[(src, dest)] = getPairBetweenZoneHelper(zones_data[src], zones_data[dest])

    return allPairZones

def allPairZoneToJSON(allPairZones):
    # Convert tuple keys to string
    allPairZonesStrKeys = {f"{src}-{dest}": value for (src, dest), value in allPairZones.items()}

    # Output to JSON
    OUTPUT_FILE_PATH = os.path.abspath("output/{}")
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH.format(OUTPUT_FILENAME_JSON)), exist_ok=True)
    with open(OUTPUT_FILE_PATH.format(OUTPUT_FILENAME_JSON), 'w', encoding="UTF-8") as file:
        json.dump(allPairZonesStrKeys, file, indent=4, ensure_ascii=False)

    print(f"Zones and their stops have been saved to {OUTPUT_FILENAME_JSON}.")



if __name__ == "__main__": 
    
    buildThisGraph()
    print("DONE BUILDING GRAPH")

    allPairZones = getPairBetweenZone()
    allPairZoneToJSON(allPairZones)
    print("DONE GETTING PAIR BETWEEN ZONES")


    
    