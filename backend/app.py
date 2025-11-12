# backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tracemalloc, time

from . import build_graph
from .utils.geo_utils import find_nearest_node
from .algorithms.bfs import bfs_path
from .algorithms.dfs import dfs_path
from .algorithms.dijkstra import dijkstra
app = Flask(__name__)
CORS(app)

# ---------- 1. Resolve shapefile path ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TXT_PATH = os.path.join(BASE_DIR, "roadFile.txt")

if not os.path.exists(TXT_PATH):
    raise FileNotFoundError(f"roadFile.txt not found at {TXT_PATH}")

with open(TXT_PATH) as f:
    shp_path = f.read().strip()

# Resolve relative paths inside roadFile.txt
if not os.path.isabs(shp_path):
    shp_path = os.path.normpath(os.path.join(BASE_DIR, shp_path))

if not os.path.exists(shp_path):
    raise FileNotFoundError(f"Shapefile not found: {shp_path}")

print(f"Using shapefile: {shp_path}")

# ---------- 2. Build graph ----------
print("Building graph... this may take a few seconds.")
graph = build_graph(shp_path)          # <-- we pass the *correct* path
nodes = list(graph.keys())
print(f"Graph loaded with {len(nodes)} nodes")

# ---------- 3. Flask routes ----------
@app.route("/route", methods=["GET"])
def route():
    try:
        start = tuple(map(float, request.args["start"].split(",")))
        end   = tuple(map(float, request.args["end"].split(",")))
        algo  = request.args.get("algo", "bfs").lower()

        start_node = find_nearest_node(start, nodes)
        end_node   = find_nearest_node(end,   nodes)

        tracemalloc.start()
        t0 = time.perf_counter()

        if algo == "bfs":
            path = bfs_path(graph, start_node, end_node)
        elif algo == "dfs":
            path = dfs_path(graph, start_node, end_node)
        elif algo == "dijkstra":
            path = dijkstra(graph, start_node, end_node)
        else:
            return jsonify({"error": "Invalid algorithm"}), 400

        t1 = time.perf_counter()
        cur, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return jsonify({
            "algorithm": algo,
            "start": start_node,
            "end": end_node,
            "path_length": len(path),
            "runtime_seconds": round(t1 - t0, 6),
            "memory_mb": round(peak / (1024*1024), 3),
            "path": path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)