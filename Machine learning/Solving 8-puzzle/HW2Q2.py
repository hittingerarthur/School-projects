import math
import pandas as pd

points = {
    "Circles": [(1, 1), (1, 3), (2, 3), (2, 5), (3, 2), (3, 3), (4, 1), (4, 4), (6, 3), (8, 1), (9,1)],
    "Squares": [(6, 2), (5, 7), (5, 9), (7, 6), (7, 7), (7, 9), (8, 7), (8, 9), (9, 4), (9, 6), (9, 8)]
}
point_to_classify = (5, 2)
distances = []

for label, point_list in points.items():
    for p in point_list:
        distance = math.sqrt((p[0] - point_to_classify[0])**2 + (p[1] - point_to_classify[1])**2)
        distances.append((distance, label, p))

distances.sort(key=lambda x: x[0])
nearest_neighbors = distances[:7]

print("7 Nearest Neighbors:")
for i, neighbor in enumerate(nearest_neighbors, start=1):
    distance, label, coords = neighbor
    print(f"{i}: Distance = {round(distance, 2)}, Class = {label}, Coordinates = {coords}")
