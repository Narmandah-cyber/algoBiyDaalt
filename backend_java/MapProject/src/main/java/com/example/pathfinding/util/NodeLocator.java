package com.example.pathfinding.util;

import com.example.pathfinding.model.Node;

import java.util.List;

public class NodeLocator {
    private final List<Node> nodes;

    public NodeLocator(List<Node> nodes) {
        this.nodes = nodes;
    }

    public Node findNearest(Node coord) {
        Node best = null;
        double bestDist = Double.POSITIVE_INFINITY;

        for (Node n : nodes) {
            double d = GeoUtils.haversine(coord, n);
            if (d < bestDist) {
                bestDist = d;
                best = n;
            }
        }
        return best;
    }

    public Node findNearest(double lon, double lat) {
        return findNearest(new Node(lon, lat));
    }
}
