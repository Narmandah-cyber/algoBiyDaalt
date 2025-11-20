import math
from scipy.spatial import KDTree

def haversine(a, b):
    lon1, lat1 = a
    lon2, lat2 = b
    R = 6371
    dlon, dlat = math.radians(lon2 - lon1), math.radians(lat2 - lat1)
    h = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(h))

class NodeLocator:
    def __init__(self, nodes):
        self.nodes = nodes
        self.tree = KDTree(nodes)

    def find_nearest(self, coord):
        _, idx = self.tree.query(coord)
        return self.nodes[idx]
