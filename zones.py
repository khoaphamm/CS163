import json

from helper.fileReader import *
from collections import defaultdict

INPUT_FILENAME = "zone_pairs.json"
OUTPUT_FILENAME_CSV = "zone_pairs.csv"
OUTPUT_FILENAME_JSON = "output_zone_pairs.json"

def getListZonePair():
    try:
        zoneGroup, filename = dataReader(INPUT_FILENAME)
        
        res = dict()
        
        for zone_pair in zoneGroup:
            if not zone_pair:
                continue
            res[zone_pair] = zoneGroup[zone_pair]

        return res
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return []