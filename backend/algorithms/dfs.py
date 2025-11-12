from typing import List, Tuple, Dict

Node = Tuple[float, float]
Graph = Dict[Node, List[Tuple[Node, float]]]


def dfs_path(graph: Graph, start: Node, goal: Node) -> List[Node]:

    if start == goal:
        return [start]

    visited = {start}
    stack: List[Tuple[Node, List[Node]]] = [(start, [start])]

    while stack:
        node, path = stack.pop()

        for neighbour, _ in graph.get(node, []):
            if neighbour in visited:
                continue
            if neighbour == goal:
                return path + [neighbour]

            visited.add(neighbour)
            stack.append((neighbour, path + [neighbour]))

    return []