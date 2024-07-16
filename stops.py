import json

from classes.Stop import *
from helper.fileReader import *
from collections import defaultdict

INPUT_FILENAME = "stops.json"
INPUT_FILENAME_ZONE = "zone_pairs.json"
OUTPUT_FILENAME_CSV = "stops.csv"
OUTPUT_FILENAME_JSON = "zone_stops.json"

def getListStop():
    try:
        stopsGroup, filename = dataReader(INPUT_FILENAME)
        
        res = list()
        
        for stops in stopsGroup:
            if not stops:
                continue
            res.append(Stop(stops))
        
        listRoutes = ListStops(res)
        return listRoutes
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return []



if __name__ == "__main__": 
    stop = getListStop()
    zones_data = defaultdict(list)
    for stops in stop.stopGroup:
        for stop in stops.Stops:
            zones_data[stop["Zone"]].append(stop)

    if zones_data is not None:
        stop.outputAsJSON(OUTPUT_FILENAME_JSON, zones_data)
    else :
        print("No result found, please try again.")