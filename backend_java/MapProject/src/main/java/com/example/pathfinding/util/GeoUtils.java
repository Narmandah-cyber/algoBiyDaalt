package com.example.pathfinding.util;

import com.example.pathfinding.model.Node;

public class GeoUtils {

    public static double haversine(Node a, Node b) {
        double lon1 = a.getLon();
        double lat1 = a.getLat();
        double lon2 = b.getLon();
        double lat2 = b.getLat();

        double R = 6371.0; // km
        double dLon = Math.toRadians(lon2 - lon1);
        double dLat = Math.toRadians(lat2 - lat1);

        double h = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(Math.toRadians(lat1)) *
                        Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);

        return 2 * R * Math.asin(Math.sqrt(h));
    }
}
