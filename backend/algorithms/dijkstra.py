import heapq
from utils.geo_utils import haversine

def dijkstra(graph, start, goal):
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        dist, node, path = heapq.heappop(pq)
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                new_dist = dist + haversine(node, neighbor)
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))
    return []
