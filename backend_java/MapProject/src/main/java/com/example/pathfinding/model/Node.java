package com.example.pathfinding.model;

import java.util.Objects;

public class Node {
    private final double lon;
    private final double lat;

    public Node(double lon, double lat) {
        this.lon = lon;
        this.lat = lat;
    }

    public double getLon() {
        return lon;
    }

    public double getLat() {
        return lat;
    }

    public double[] toArray() {
        return new double[]{lon, lat};
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Node node = (Node) o;
        return Double.compare(node.lon, lon) == 0 &&
                Double.compare(node.lat, lat) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(lon, lat);
    }

    @Override
    public String toString() {
        return "Node(" + lon + ", " + lat + ")";
    }
}
