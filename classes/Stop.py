class Stop: 
  def __init__(self, stops):
    for key, value in stops.items():
      setattr(self, key, value)
  

class ListStops():
  def __init__(self, allStop):
    self.allStops = allStop