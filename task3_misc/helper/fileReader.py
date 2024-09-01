import os
import json

INPUT_FILE_PATH = os.path.abspath("data/{}")
OUTPUT_FILE_PATH = os.path.abspath("output/{}")

def dataReader(INPUT_FILENAME):
  with open(INPUT_FILE_PATH.format(INPUT_FILENAME), 'r') as f:
    data = json.load(f)
    return data, INPUT_FILE_PATH.format(INPUT_FILENAME)
  
def dataWriter(data, OUTPUT_FILENAME):
  with open(OUTPUT_FILE_PATH.format(OUTPUT_FILENAME), 'w') as f:
    json.dump(data, f)
    return OUTPUT_FILE_PATH.format(OUTPUT_FILENAME)