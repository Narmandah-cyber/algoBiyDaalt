import geopandas as gpd
from shapely.geometry import LineString
from collections import defaultdict

def build_graph(shp_path):
    roads = gpd.read_file(shp_path)
    graph = defaultdict(list)

    for _, row in roads.iterrows():
        geom = row.geometry
        if not isinstance(geom, LineString):
            continue

        coords = list(geom.coords)
        oneway = row.get("oneway", "no")

        for i in range(len(coords) - 1):
            start, end = tuple(coords[i]), tuple(coords[i + 1])
            graph[start].append(end)
            if oneway != "yes":
                graph[end].append(start)
    return graph
