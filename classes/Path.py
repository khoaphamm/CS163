
class Path: 
    def __init__(self, path):
        for key, value in path.items():
            setattr(self, key, value)

    def setProperty(self, key, value):
        setattr(self, key, value)

class ListPath():
    def __init__(self, pathGroup):
        self.pathGroup = pathGroup