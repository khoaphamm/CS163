from helper.fileReader import dataReader, dataWriter

data, filename = dataReader("trace_trips2.json")

total_edges = len(data)

sum_edges = 0

for edge in data:
    sum_edges += len(data[edge])

print(f"Total edges: {total_edges}")
print(f"Total trips: {sum_edges}")
print(f"Average trips per edge: {sum_edges/total_edges}")
