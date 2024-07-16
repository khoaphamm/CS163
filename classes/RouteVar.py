class RouteVar:
    def __init__(self, routes):
        self.routeVar = routes
          
    def setProperty(self, key, value):
        setattr(self, key, value)
        

class ListRouteVar():
    def __init__(self, routeGroup):
        self.routeGroup = routeGroup