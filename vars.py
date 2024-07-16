import json
from classes.RouteVar import * 
from helper.fileReader import dataReader

INPUT_FILENAME = "vars.json"


def getListRoute():
    try:
        routesGroup, filename = dataReader(INPUT_FILENAME)
        
        listRoute = list()
        for route in routesGroup:
            # print(type(route), route)
            
            listRoute.append(RouteVar(route))
        
        listRoute = ListRouteVar(listRoute)

        return listRoute
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return []