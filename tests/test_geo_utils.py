import pytest
from backend.utils.geo_utils import haversine, find_nearest_node


def test_haversine_zero_distance():
    p = (106.9, 47.9)
    assert haversine(p, p) == 0.0


def test_haversine_positive_distance():
    """
    Distance between (106.9, 47.9) and (107.0, 47.9)
    → 0.1° longitude at latitude 47.9° ≈ 7.45 km
    """
    a = (106.9, 47.9)
    b = (107.0, 47.9)
    d = haversine(a, b)
    assert 7.4 < d < 7.5, f"Expected ~7.45 km, got {d:.3f} km"


def test_find_nearest_node():
    """Should return the closest node by haversine distance."""
    nodes = [(106.9, 47.9), (107.1, 47.9), (106.95, 47.85)]
    coord = (106.91, 47.9)
    nearest = find_nearest_node(coord, nodes)
    assert nearest == (106.9, 47.9)


def test_find_nearest_node_empty_list():
    """Should raise ValueError if nodes list is empty."""
    with pytest.raises(ValueError):
        find_nearest_node((0, 0), [])