from collections import deque

def bfs_path(graph, start, goal):
    """
    BFS ignores weights and only uses graph structure.
    """
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            # only neighbor nodes, ignore weights
            for neighbor in [n if isinstance(n, tuple) else n[0] for n in graph[node]]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return []
