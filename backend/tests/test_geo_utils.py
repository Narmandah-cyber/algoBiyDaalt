from utils.geo_utils import haversine, find_nearest_node

def test_haversine_zero_distance():
    a = (106.9, 47.9)
    assert haversine(a, a) == 0

def test_haversine_positive():
    a = (106.9, 47.9)
    b = (107.0, 47.9)
    assert haversine(a, b) > 0

def test_find_nearest_node():
    nodes = [(106.9, 47.9), (107.1, 47.9)]
    coord = (106.91, 47.9)
    nearest = find_nearest_node(coord, nodes)
    assert nearest == (106.9, 47.9)
