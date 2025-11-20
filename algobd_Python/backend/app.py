import os, time, tracemalloc
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import build_graph
from .utils.geo_utils import NodeLocator
from .algorithms.bfs import bfs_path
from .algorithms.dfs import dfs_path
from .algorithms.dijkstra import dijkstra

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TXT_PATH = os.path.join(BASE_DIR, "roadFile.txt")
if not os.path.exists(TXT_PATH):
    raise FileNotFoundError(f"roadFile.txt not found at {TXT_PATH}")

with open(TXT_PATH) as f:
    shp_path = f.read().strip()
if not os.path.isabs(shp_path):
    shp_path = os.path.join(BASE_DIR, shp_path)
if not os.path.exists(shp_path):
    raise FileNotFoundError(f"Shapefile not found: {shp_path}")

print(f"Using shapefile: {shp_path}")
print("Building graph... Please wait.")
graph = build_graph(shp_path)
nodes = list(graph.keys())
locator = NodeLocator(nodes)
print(f"Graph loaded with {len(nodes)} nodes")

@app.route("/route", methods=["GET"])
def route():
    try:
        start = tuple(map(float, request.args["start"].split(",")))
        end = tuple(map(float, request.args["end"].split(",")))
        algo = request.args.get("algo", "bfs").lower()

        start_node = locator.find_nearest(start)
        end_node = locator.find_nearest(end)

        tracemalloc.start()
        t0 = time.perf_counter()

        if algo == "bfs":
            path = bfs_path(graph, start_node, end_node)
            complexity_time = "O(V + E)"
            complexity_space = "O(V)"
        elif algo == "dfs":
            path = dfs_path(graph, start_node, end_node)
            complexity_time = "O(V + E)"
            complexity_space = "O(V)"
        elif algo == "dijkstra":
            path = dijkstra(graph, start_node, end_node)
            complexity_time = "O((V + E) log V)"
            complexity_space = "O(V + E)"
        else:
            return jsonify({"error": "Invalid algorithm"}), 400

        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return jsonify({
            "algorithm": algo,
            "path_length": len(path),
            "runtime_seconds": round(t1 - t0, 6),
            "memory_mb": round(peak / (1024*1024), 3),
            "path": path,
            "complexity_time": complexity_time,
            "complexity_space": complexity_space
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
