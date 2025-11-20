from collections import deque
from typing import List, Tuple, Dict

Node = Tuple[float, float]
Graph = Dict[Node, List[Tuple[Node, float]]]

def bfs_path(graph: Graph, start: Node, goal: Node) -> List[Node]:
    if start == goal:
        return [start]
    visited = {start}
    parent = {start: None}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        for neigh, _ in graph.get(node, []):
            if neigh in visited:
                continue
            visited.add(neigh)
            parent[neigh] = node
            if neigh == goal:
                return reconstruct_path(parent, start, goal)
            queue.append(neigh)
    return []

def reconstruct_path(parent, start, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path
