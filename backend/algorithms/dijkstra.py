import heapq

def dijkstra(graph, start, goal):
    """
    Weighted Dijkstra algorithm for realistic shortest path.
    Graph edges are in the form: node -> [(neighbor, weight), ...]
    """
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        total_weight, node, path = heapq.heappop(pq)
        if node == goal:
            return path

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (total_weight + weight, neighbor, path + [neighbor]))

    return []
