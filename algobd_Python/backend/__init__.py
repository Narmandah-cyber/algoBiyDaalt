import os
from collections import defaultdict
import geopandas as gpd
from shapely import LineString
from .utils.geo_utils import haversine

def build_graph(shp_path=None):
    if shp_path is None:
        current_dir = os.path.dirname(__file__)
        shp_path = os.path.normpath(
            os.path.join(current_dir, "..", "roadShapeFiles", "gis_osm_roads_free_1.shp")
        )

    if not os.path.exists(shp_path):
        raise FileNotFoundError(f"Shapefile not found: {shp_path}")

    roads = gpd.read_file(shp_path)
    graph = defaultdict(list)

    for _, row in roads.iterrows():
        geom = row.geometry
        if not isinstance(geom, LineString):
            continue

        oneway = str(row.get("oneway", "no")).lower()
        maxspeed = row.get("maxspeed", 60)
        fclass = str(row.get("fclass", "")).lower()
        surface = str(row.get("surface", "")).lower()

        try:
            speed = float(maxspeed)
        except (ValueError, TypeError):
            speed = 60.0

        if speed <= 0:
            speed = 1.0

        type_factor = 1.0
        if "motorway" in fclass:
            type_factor = 0.8
        elif "trunk" in fclass:
            type_factor = 0.9
        elif "residential" in fclass:
            type_factor = 1.2
        elif "service" in fclass or "track" in fclass:
            type_factor = 1.5

        if "gravel" in surface or "dirt" in surface:
            type_factor *= 1.3

        if type_factor == 0:
            type_factor = 1.0

        coords = list(geom.coords)
        for i in range(len(coords) - 1):
            start, end = tuple(coords[i]), tuple(coords[i + 1])
            dist_km = haversine(start, end)

            denominator = (speed / 60 / type_factor)
            if denominator == 0:
                denominator = 1e-6

            weight = dist_km / denominator

            graph[start].append((end, weight))
            if oneway != "yes":
                graph[end].append((start, weight))

    return graph
