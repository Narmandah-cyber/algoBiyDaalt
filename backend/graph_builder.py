import geopandas as gpd
from shapely.geometry import LineString
from collections import defaultdict
from utils.geo_utils import haversine


def build_graph(shp_path):
    """
    Build a realistic weighted road graph from OSM shapefile.
    Each edge stores (neighbor_node, travel_weight)
    """
    roads = gpd.read_file(shp_path)
    graph = defaultdict(list)

    for _, row in roads.iterrows():
        geom = row.geometry
        if not isinstance(geom, LineString):
            continue

        oneway = str(row.get("oneway", "no")).lower()
        maxspeed = row.get("maxspeed", 60)
        access = str(row.get("access", "yes")).lower()
        fclass = str(row.get("fclass", "")).lower()
        surface = str(row.get("surface", "")).lower()

        # Skip if road is not accessible by car
        if "no" in access or "foot" in access or "bicycle" in access:
            continue

        # Default speed
        try:
            speed = float(maxspeed)
        except (ValueError, TypeError):
            speed = 60.0

        # Adjust weight factor based on road type (fclass)
        type_factor = 1.0
        if "motorway" in fclass:
            type_factor = 0.8
        elif "trunk" in fclass:
            type_factor = 0.9
        elif "primary" in fclass:
            type_factor = 1.0
        elif "residential" in fclass:
            type_factor = 1.2
        elif "service" in fclass or "track" in fclass:
            type_factor = 1.5

        # Adjust based on surface
        if "gravel" in surface or "dirt" in surface:
            type_factor *= 1.3
        elif "paved" in surface or "asphalt" in surface:
            type_factor *= 1.0

        # Build graph edges
        coords = list(geom.coords)
        for i in range(len(coords) - 1):
            start = tuple(coords[i])
            end = tuple(coords[i + 1])
            dist_km = haversine(start, end)

            # Prevent division by zero or invalid data
            if not isinstance(speed, (int, float)) or speed <= 0:
                speed = 60.0
            if type_factor <= 0:
                type_factor = 1.0

            # Travel time (minutes)
            weight = dist_km / (speed / 60 / type_factor)

            graph[start].append((end, weight))
            if oneway != "yes":
                graph[end].append((start, weight))

    return graph
