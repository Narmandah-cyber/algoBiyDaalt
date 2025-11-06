from flask import Flask, request, jsonify
import tracemalloc, time
from flask_cors import CORS 

from graph_builder import build_graph
from utils.geo_utils import find_nearest_node
from algorithms.bfs import bfs_path
from algorithms.dfs import dfs_path
from algorithms.dijkstra import dijkstra

app = Flask(__name__)
CORS(app)  

with open("roadFile.txt") as f:
    shp_path = f.read().strip()
graph = build_graph(shp_path)
nodes = list(graph.keys())

@app.route("/route", methods=["GET"])
def route():
    try:
        start = tuple(map(float, request.args["start"].split(",")))
        end = tuple(map(float, request.args["end"].split(",")))
        algo = request.args.get("algo", "bfs").lower()

        start_node = find_nearest_node(start, nodes)
        end_node = find_nearest_node(end, nodes)

        # Start measuring performance
        tracemalloc.start()
        start_time = time.perf_counter()

        # Choose algorithm
        if algo == "bfs":
            path = bfs_path(graph, start_node, end_node)
        elif algo == "dfs":
            path = dfs_path(graph, start_node, end_node)
        elif algo == "dijkstra":
            path = dijkstra(graph, start_node, end_node)
        else:
            return jsonify({"error": "Invalid algorithm"}), 400

        # Stop performance tracking
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        runtime = end_time - start_time
        memory_mb = peak / (1024 * 1024)

        return jsonify({
            "algorithm": algo,
            "start": start_node,
            "end": end_node,
            "path_length": len(path),
            "runtime_seconds": round(runtime, 6),
            "memory_mb": round(memory_mb, 3),
            "path": path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
