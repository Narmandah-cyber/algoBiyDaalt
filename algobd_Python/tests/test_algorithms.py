from backend.algorithms.bfs import bfs_path
from backend.algorithms.dfs import dfs_path
from backend.algorithms.dijkstra import dijkstra

A = (0.0, 0.0)
B = (1.0, 0.0)
C = (2.0, 0.0)
D = (0.0, 1.0)

test_graph = {
    A: [(B, 1.0), (D, 2.0)],           # A → B (1 min), A → D (2 min)
    B: [(A, 1.0), (C, 1.0), (D, 1.5)], # B → C (1 min), B → D (1.5 min)
    C: [(B, 1.0)],
    D: [(A, 2.0), (B, 1.5)]
}
def test_bfs_shortest_node_count():
    path = bfs_path(test_graph, A, C)
    assert path == [A, B, C], f"BFS returned {path}"
    assert len(path) == 3


def test_bfs_same_node():
    path = bfs_path(test_graph, A, A)
    assert path == [A]


def test_bfs_no_path():
    isolated = (99.0, 99.0)
    path = bfs_path(test_graph, A, isolated)
    assert path == []

def test_dfs_finds_a_path():
    path = dfs_path(test_graph, A, C)
    assert path[0] == A
    assert path[-1] == C
    assert len(path) >= 2   # at least one edge


def test_dfs_same_node():
    path = dfs_path(test_graph, A, A)
    assert path == [A]


def test_dfs_no_path():
    isolated = (99.0, 99.0)
    path = dfs_path(test_graph, A, isolated)
    assert path == []


def test_dijkstra_fastest_path():
    # A → B → C = 1 + 1 = 2 min
    # A → D → B → C = 2 + 1.5 + 1 = 4.5 min → slower
    path = dijkstra(test_graph, A, C)
    assert path == [A, B, C], f"Dijkstra returned {path}"


def test_dijkstra_same_node():
    path = dijkstra(test_graph, A, A)
    assert path == [A]


def test_dijkstra_no_path():
    isolated = (99.0, 99.0)
    path = dijkstra(test_graph, A, isolated)
    assert path == []


def test_empty_graph():
    empty: dict = {}
    assert bfs_path(empty, A, C) == []
    assert dfs_path(empty, A, C) == []
    assert dijkstra(empty, A, C) == []