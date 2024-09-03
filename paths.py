import json
from classes.Path import *
from helper.fileReader import dataReader

INPUT_FILENAME = "paths.json"


def getListPath():
    try:
        routesGroup, filename = dataReader(INPUT_FILENAME)
        res = list()
        
        for routes in routesGroup:
          if not routes:
            continue
          res.append(Path(routes))
        
        # Assuming RouteVarQuery processes the list of routes in some way
        listPath = ListPath(res)
        return listPath
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return []
  

