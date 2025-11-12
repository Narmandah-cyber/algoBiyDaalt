import heapq
from typing import List, Tuple, Dict

Node = Tuple[float, float]
Graph = Dict[Node, List[Tuple[Node, float]]]


def dijkstra(graph: Graph, start: Node, goal: Node) -> List[Node]:

    if start == goal:
        return [start]

    pq: List[Tuple[float, Node, List[Node]]] = [(0.0, start, [start])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        if node == goal:
            return path

        visited.add(node)
        for neigh, weight in graph.get(node, []):
            if neigh not in visited:
                heapq.heappush(pq, (cost + weight, neigh, path + [neigh]))

    return []