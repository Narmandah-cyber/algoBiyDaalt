from collections import deque
from typing import List, Tuple, Dict, Any

Node = Tuple[float, float]                # (lon, lat)
Graph = Dict[Node, List[Tuple[Node, float]]]


def bfs_path(graph: Graph, start: Node, goal: Node) -> List[Node]:

    if start == goal:
        return [start]

    visited = {start}
    queue: deque[Tuple[Node, List[Node]]] = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        # neighbours are already tuples (node, weight)
        for neighbour, _ in graph.get(node, []):
            if neighbour in visited:
                continue
            if neighbour == goal:
                return path + [neighbour]

            visited.add(neighbour)
            queue.append((neighbour, path + [neighbour]))

    return []      # no path