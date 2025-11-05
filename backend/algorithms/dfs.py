def dfs_path(graph, start, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = [start]

    visited.add(start)
    if start == goal:
        return path

    for neighbor in graph[start]:
        if neighbor not in visited:
            new_path = dfs_path(graph, neighbor, goal, visited, path + [neighbor])
            if new_path:
                return new_path
    return []
