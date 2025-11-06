import math
import pytest
from algorithms.bfs import bfs_path
from algorithms.dfs import dfs_path
from algorithms.dijkstra import dijkstra

# Small manual test graph
#   A ---1--- B ---1--- C
#    \        |
#     \---2---D
graph = {
    "A": ["B", "D"],
    "B": ["A", "C", "D"],
    "C": ["B"],
    "D": ["A", "B"]
}

coords = {
    "A": (0, 0),
    "B": (1, 0),
    "C": (2, 0),
    "D": (0, 1)
}

def fake_haversine(a, b):
    (x1, y1), (x2, y2) = coords[a], coords[b]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def test_bfs_path():
    path = bfs_path(graph, "A", "C")
    assert path == ["A", "B", "C"], f"BFS path incorrect: {path}"

def test_dfs_path():
    path = dfs_path(graph, "A", "C")
    assert "A" in path and "C" in path, "DFS must contain A and C"
    assert path[0] == "A", "DFS must start at A"

def test_dijkstra_path(monkeypatch):
    from algorithms import dijkstra as dj
    monkeypatch.setattr(dj, "haversine", fake_haversine)

    path = dijkstra(graph, "A", "C")
    assert path == ["A", "B", "C"], f"Dijkstra shortest path incorrect: {path}"

def test_bfs_same_node():
    path = bfs_path(graph, "A", "A")
    assert path == ["A"], "Path to same node should be itself"
