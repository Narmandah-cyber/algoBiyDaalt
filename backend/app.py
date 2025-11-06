from flask import Flask, request, jsonify
from flask_cors import CORS
import tracemalloc, time

from graph_builder import build_graph
from utils.geo_utils import find_nearest_node
from algorithms.bfs import bfs_path
from algorithms.dfs import dfs_path
from algorithms.dijkstra import dijkstra

app = Flask(__name__)
CORS(app)

# Load map data and build weighted graph
with open("roadFile.txt") as f:
    shp_path = f.read().strip()

print("Building graph... this may take a few seconds.")
graph = build_graph(shp_path)
nodes = list(graph.keys())
print(f"Graph loaded with {len(nodes)} nodes")

@app.route("/route", methods=["GET"])
def route():
    try:
        start = tuple(map(float, request.args["start"].split(",")))
        end = tuple(map(float, request.args["end"].split(",")))
        algo = request.args.get("algo", "bfs").lower()

        start_node = find_nearest_node(start, nodes)
        end_node = find_nearest_node(end, nodes)

        tracemalloc.start()
        start_time = time.perf_counter()

        if algo == "bfs":
            path = bfs_path(graph, start_node, end_node)
        elif algo == "dfs":
            path = dfs_path(graph, start_node, end_node)
        elif algo == "dijkstra":
            path = dijkstra(graph, start_node, end_node)
        else:
            return jsonify({"error": "Invalid algorithm"}), 400

        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        runtime = round(end_time - start_time, 6)
        memory_mb = round(peak / (1024 * 1024), 3)

        return jsonify({
            "algorithm": algo,
            "start": start_node,
            "end": end_node,
            "path_length": len(path),
            "runtime_seconds": runtime,
            "memory_mb": memory_mb,
            "path": path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
