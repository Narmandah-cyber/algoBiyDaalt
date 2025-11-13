import heapq
from typing import List, Tuple, Dict

Node = Tuple[float, float]
Graph = Dict[Node, List[Tuple[Node, float]]]

def dijkstra(graph: Graph, start: Node, goal: Node) -> List[Node]:
    if start == goal:
        return [start]
    pq = [(0.0, start)]
    dist = {start: 0.0}
    parent = {start: None}
    visited = set()

    while pq:
        cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return reconstruct_path(parent, start, goal)

        for neigh, weight in graph.get(node, []):
            new_cost = cost + weight
            if neigh not in dist or new_cost < dist[neigh]:
                dist[neigh] = new_cost
                parent[neigh] = node
                heapq.heappush(pq, (new_cost, neigh))
    return []

def reconstruct_path(parent, start, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path
