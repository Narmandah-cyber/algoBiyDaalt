from typing import List, Tuple, Dict

Node = Tuple[float, float]
Graph = Dict[Node, List[Tuple[Node, float]]]

def dfs_path(graph: Graph, start: Node, goal: Node) -> List[Node]:
    if start == goal:
        return [start]
    visited = {start}
    parent = {start: None}
    stack = [start]

    while stack:
        node = stack.pop()
        for neigh, _ in graph.get(node, []):
            if neigh in visited:
                continue
            visited.add(neigh)
            parent[neigh] = node
            if neigh == goal:
                return reconstruct_path(parent, start, goal)
            stack.append(neigh)
    return []

def reconstruct_path(parent, start, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path
