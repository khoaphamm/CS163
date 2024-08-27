from stops import getListStop
from zones import getListZonePair
from vars import getListRoute
from paths import getListPath

from helper.compute import *
from classes.Graph import *
import random
import folium 
from folium import CustomIcon
import time

listRoute = getListRoute()
listStop = getListStop()
listPath = getListPath()
listZonePair = getListZonePair()

g = Graph()

def findRawDistance(u, v):
  XI, YI = g.position[u]
  XD, YD = g.position[v]

  distance = 0.0

  if not (XI == None or YI == None or XD == None or YD == None):
    distance += sqrt((XI - XD)**2 + (YI - YD)**2)

  return distance

def buildGraph():
  
  totalTimeBase = 0
  stopCount = 0

  for stopData in listStop.allStops:
      stopCount += 1
      routeId, routeVarId = int(stopData.RouteId), int(stopData.RouteVarId)
      runningTime, totalDistance = None, None

      # Find matching route and extract running time and distance
      for routeGroup in listRoute.routeGroup:
          routeDetails = routeGroup.routeVar
          if routeDetails["RouteId"] == routeId:
              runningTime, totalDistance = routeDetails["RunningTime"], routeDetails["Distance"]
              break

      if runningTime is None or totalDistance is None:
          continue

      # Select path with matching RouteId and RouteVarId
      selectedPath = next((path for path in listPath.pathGroup if int(path.RouteId) == routeId and int(path.RouteVarId) == routeVarId), None)
      if selectedPath is None:
          continue

      # Convert running time to seconds and calculate base time per distance unit
      runningTimeInSeconds = runningTime * 60
      baseTimePerUnitDistance = runningTimeInSeconds / totalDistance
      totalTimeBase += baseTimePerUnitDistance

      # Initialize graph with the first stop
      g.set_node(stopData.Stops[0]["StopId"], stopData.Stops[0])

      # Iterate through stops to calculate distances and time costs
      for i in range(len(stopData.Stops) - 1):
          longitudePath, latitudePath = [], []

          distance = findDistance(selectedPath, longitudePath, latitudePath, stopData.Stops[i], stopData.Stops[i + 1])
          timeCost = distance * baseTimePerUnitDistance

          # Add edge between consecutive stops
          g.add_edge(stopData.Stops[i]["StopId"], stopData.Stops[i + 1]["StopId"], (timeCost, distance, routeId, routeVarId, longitudePath, latitudePath))
          # Update graph with the next stop
          g.set_node(stopData.Stops[i + 1]["StopId"], stopData.Stops[i + 1])

  # print("Average time base: ", totalTimeBase / stopCount)  

def shortestPathA(start, end):
  if start is None or end is None:
      return None

  g.reset_graph()
  # Use A* algorithm for pathfinding
  path_stops = g.astar(start, end)

  path_details = {
      "StartStopId": start,
      "EndStopId": end,
      "RunningTime": g.distances[end]
  }

  path_stop_ids = []
  current_stop = end
  while current_stop != -1 and start != current_stop:
      path_stop_ids.append(current_stop)
      current_stop = g.predecessors[current_stop]
      if start == current_stop:
          path_stop_ids.append(current_stop)
          break
  path_stop_ids.reverse()

  path_details["StopIds"] = path_stop_ids

  path_route_info = []
  for stop_id in path_stop_ids:
      if g.route_data[stop_id]:
          stop_info = {
              "lat": g.path_data[stop_id][1],
              "lng": g.path_data[stop_id][0],
              "RouteId": g.route_data[stop_id][0],
              "RouteVarId": g.route_data[stop_id][1]
          }
          path_route_info.append(stop_info)

  path_details["Path"] = path_route_info

  return path_details, path_stops

def shortestPathD(start, end):
  if start is None or end is None:
      return None

  g.reset_graph()
  # Use Dijkstra algorithm for pathfinding
  path_stops = g.dijkstra(start, end)

  path_details = {
      "StartStopId": start,
      "EndStopId": end,
      "RunningTime": g.distances[end]
  }

  path_stop_ids = []
  current_stop = end
  while current_stop != -1 and start != current_stop:
      path_stop_ids.append(current_stop)
      current_stop = g.predecessors[current_stop]
      if start == current_stop:
          path_stop_ids.append(current_stop)
          break
  path_stop_ids.reverse()

  path_details["StopIds"] = path_stop_ids

  path_route_info = []
  for stop_id in path_stop_ids:
      if g.route_data[stop_id]:
          stop_info = {
              "lat": g.path_data[stop_id][1],
              "lng": g.path_data[stop_id][0],
              "RouteId": g.route_data[stop_id][0],
              "RouteVarId": g.route_data[stop_id][1]
          }
          path_route_info.append(stop_info)

  path_details["Path"] = path_route_info

  return path_details, path_stops

def shortestPathWithCaching(u, v):
  if u == None or v == None: return
  startZone = g.stops_data[u]["Zone"]
  endZone = g.stops_data[v]["Zone"]

  if findRawDistance(u, v) < 4000 or startZone == endZone:
    return shortestPathA(u, v)
  else:
    search_key = f"{startZone}-{endZone}"
   
    cached_path = listZonePair[search_key]
    if not cached_path or "Học Sinh" in search_key:
      return shortestPathA(u, v)
    else:
      res = dict()
      stops = list()
      res["StartStopId"] = u
      res["EndStopId"] = v

      fixed_stop_start_zone = cached_path["StartStopId"]
      fixed_stop_end_zone = cached_path["EndStopId"]

      route1, first_stops_visited = shortestPathA(u, fixed_stop_start_zone)
      route2 = cached_path
      route3, second_stops_visited = shortestPathA(fixed_stop_end_zone, v)

      stops.extend(first_stops_visited)
      for stop in cached_path["StopIds"][1:-1]:
          stops.append(stop) 
      stops.extend(second_stops_visited)

      total_time = route1["RunningTime"] + route2["RunningTime"] + route3["RunningTime"]
      res["RunningTime"] = total_time

      res["StopIds"] = route1["StopIds"].copy()  # Start with a copy of route1["StopIds"]
      # trim the first element of route2["StopIds"] because it is the same as the last element of route1["StopIds"]
      res["StopIds"].extend(route2["StopIds"][1:])
      res["StopIds"].extend(route3["StopIds"][1:])  # Extend with route3["StopIds"]

      res["Path"] = route1["Path"].copy()  # Start with a copy of route1["Path"]
      res["Path"].extend(route2["Path"])  # Extend with route2["Path"]
      res["Path"].extend(route3["Path"])  # Extend with route3["Path"]

      
      return res, stops
 

def getAllStop():
    allStop = dict()
    for stop_group in listStop.allStops:
        if not stop_group:
            continue
        for stop in stop_group.Stops:
            allStop[stop["StopId"]] = stop

    return allStop

def drawOnMap(res, stops):
  #Draw on maps
  m = folium.Map(location=[res["Path"][0]["lat"][0], res["Path"][0]["lng"][0]], zoom_start=13)
  
  stopId = res["StartStopId"]

  stop = g.stops_data[stopId]
  lat, lng = stop["Lat"], stop["Lng"]
  folium.Marker((lat, lng), 
                  popup=f"{stop['Name']} ({stop['StopId']})",
                  tooltip=stop['Name']).add_to(m)
  
  stopId = res["EndStopId"]

  stop = g.stops_data[stopId]
  lat, lng = stop["Lat"], stop["Lng"]
  folium.Marker((lat, lng), 
                  popup=f"{stop['Name']} ({stop['StopId']})",
                  tooltip=stop['Name']).add_to(m)
  # # 2561 4274
  # # 1431 476
  # # 1431 7626
  # 7673 730
  # 2419 4424

  for path in res["Path"]:
    # Directly use the lat and lng values to create a point tuple
    points = list(zip(path["lat"], path["lng"]))
    if not points: continue
    # Since PolyLine expects a list of points, we wrap our single point in a list
    folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(m)

  ## Add all stops visited to the map
  for stopId in stops:
    stop = g.stops_data[stopId]
    lat, lng = stop["Lat"], stop["Lng"]
    # folium.Marker((lat, lng), 
    #               popup=f"{stop['Name']} ({stop['StopId']})",
    #               tooltip=stop['Name']).add_to(m)
    folium.CircleMarker(
        location=(lat, lng),
        radius=5,
        color='black',
        fill=True,
        fill_color='red',
        opacity=0.3,
        fill_opacity=0.3,  # Set the fill opacity to make it less visible
        popup=folium.Popup(f"{stop['Name']} ({stop['StopId']})"),
        tooltip=stop['Name']
    ).add_to(m)
    
  # To save the map
  print(stops.__len__())
  m.save('map.html')

  # save in json to be implemented

def measure_performance(test_cases):
    times_no_cache = []
    times_with_cache = []

    total_stops_no_cache = 0
    total_stops_with_cache = 0
   
    for start, end in test_cases:
        # Measure shortestPath
        start_time = time.time()
        a, Estops = shortestPathA(start, end)
        end_time = time.time()
        times_no_cache.append(end_time - start_time)
        total_stops_no_cache += len(Estops)

        # Measure shortestPathWithCaching
        start_time = time.time()
        b, Astops = shortestPathWithCaching(start, end)
        end_time = time.time()
        times_with_cache.append(end_time - start_time)
        total_stops_with_cache += len(Astops)
        # print(len(Estops), len(Astops))

    average_stops_no_cache = total_stops_no_cache / len(test_cases)
    average_stops_with_cache = total_stops_with_cache / len(test_cases)
    
    return times_no_cache, times_with_cache, average_stops_no_cache, average_stops_with_cache



if __name__ == "__main__":
  
  # 1. Build graph
  buildGraph()
  print("DONE BUILDING GRAPH")

  test_cases = []

  # 2. Measure performance
  number_of_test_cases = 100

  while(len(test_cases) < number_of_test_cases):
    u = random.randint(0, 9999)
    v = random.randint(0, 9999)
    if u == v or (u, v) in test_cases or (v, u) in test_cases or not g.stops_data[u] or not g.stops_data[v]:
      continue
    test_cases.append((u, v))

  times_no_cache, times_with_cache, ave1, ave2 = measure_performance(test_cases)

  # Print or analyze the results
  total_no_cache = sum(times_no_cache)
  total_with_cache = sum(times_with_cache)
  average_no_cache = total_no_cache / len(times_no_cache)
  average_with_cache = total_with_cache / len(times_with_cache)

  for i, (t_no_cache, t_with_cache) in enumerate(zip(times_no_cache, times_with_cache)):
      print(f"Test Case {i+1}: No Cache = {t_no_cache}s, With Cache = {t_with_cache}s")

  print(f"Average Time (No Cache): {total_no_cache}s")
  print(f"Average Time (With Cache): {total_with_cache}s")
  print(f"Average Stops Visited (No Cache): {ave1}")
  print(f"Average Stops Visited (With Cache): {ave2}")

  # 3. Print shortest path from startStop to endStop

  # startStop = input("Enter start stop: ")
  # endStop = input("Enter end stop: ")
  # startStop = int(startStop)
  # endStop = int(endStop)

  # for start, end in test_cases:
  #   path, stops = shortestPathWithCaching(start, end)
  #   if stops.__len__() > 200 and stops.__len__() < 300:
  #      drawOnMap(path, stops)
  #      break
  # path, stops = shortestPathWithCaching(startStop, endStop)

  # drawOnMap(path, stops)
  
