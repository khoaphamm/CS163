import pyproj
from math import sqrt

wgs84_crs = pyproj.CRS("EPSG:4326")
utm_vn_crs = pyproj.CRS("EPSG:3405")
transformer = pyproj.Transformer.from_proj(wgs84_crs, utm_vn_crs, always_xy=True)

def convert_lnglat_to_xy(lng, lat):
    if lng is None or lat is None:
        return None, None
    x, y = transformer.transform(lng, lat)
    return x, y

# tolerance = 1e-3.5
def almost_equal(a, b, tolerance= 0.00031622776):
    return abs(a - b) < tolerance


def findDistance(path, longitudes, latitudes, startData, endData):
  isCalculating = False
  totalDistance = 0.0
  for index in range(len(path.lng)):
      if isCalculating:
          prevX, prevY = convert_lnglat_to_xy(path.lng[index - 1], path.lat[index - 1])
          currentX, currentY = convert_lnglat_to_xy(path.lng[index], path.lat[index])
          if None not in [prevX, prevY, currentX, currentY]:
              totalDistance += sqrt((prevX - currentX) ** 2 + (prevY - currentY) ** 2)

      if almost_equal(path.lng[index], startData["Lng"]) and almost_equal(path.lat[index], startData["Lat"]):
          isCalculating = True

      if isCalculating:
          longitudes.append(path.lng[index])
          latitudes.append(path.lat[index])

      if almost_equal(path.lng[index], endData["Lng"]) and almost_equal(path.lat[index], endData["Lat"]):
          break

  return totalDistance


