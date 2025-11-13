package com.example.pathfinding.graph;

import com.example.pathfinding.model.Edge;
import com.example.pathfinding.model.Node;
import com.example.pathfinding.util.GeoUtils;
import org.geotools.data.DataStore;
import org.geotools.data.DataStoreFinder;
import org.geotools.data.simple.SimpleFeatureCollection;
import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.data.simple.SimpleFeatureSource;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.LineString;
import org.opengis.feature.simple.SimpleFeature;

import java.io.File;
import java.net.URL;
import java.util.*;

public class GraphBuilder {

    public static Map<Node, List<Edge>> buildGraph(File shpFile) throws Exception {
        if (!shpFile.exists()) {
            throw new IllegalArgumentException("Shapefile not found: " + shpFile.getAbsolutePath());
        }

        Map<String, Object> params = new HashMap<String, Object>();
        URL url = shpFile.toURI().toURL();
        params.put("url", url);

        DataStore dataStore = DataStoreFinder.getDataStore(params);
        if (dataStore == null) {
            throw new RuntimeException("Could not open shapefile datastore");
        }

        String typeName = dataStore.getTypeNames()[0];
        SimpleFeatureSource source = dataStore.getFeatureSource(typeName);
        SimpleFeatureCollection collection = source.getFeatures();

        Map<Node, List<Edge>> graph = new HashMap<Node, List<Edge>>();

        try (SimpleFeatureIterator features = collection.features()) {
            while (features.hasNext()) {
                SimpleFeature feature = features.next();
                Object geomObj = feature.getDefaultGeometry();
                if (!(geomObj instanceof LineString)) {
                    continue;
                }
                LineString line = (LineString) geomObj;

                String oneway = toLowerStr(feature.getAttribute("oneway"), "no");
                String fclass = toLowerStr(feature.getAttribute("fclass"), "");
                String surface = toLowerStr(feature.getAttribute("surface"), "");

                double speed = parseSpeed(feature.getAttribute("maxspeed"));
                if (speed <= 0) speed = 1.0;

                double typeFactor = 1.0;
                if (fclass.contains("motorway")) {
                    typeFactor = 0.8;
                } else if (fclass.contains("trunk")) {
                    typeFactor = 0.9;
                } else if (fclass.contains("residential")) {
                    typeFactor = 1.2;
                } else if (fclass.contains("service") || fclass.contains("track")) {
                    typeFactor = 1.5;
                }

                if (surface.contains("gravel") || surface.contains("dirt")) {
                    typeFactor *= 1.3;
                }

                if (typeFactor == 0) typeFactor = 1.0;

                Coordinate[] coords = line.getCoordinates();
                for (int i = 0; i < coords.length - 1; i++) {
                    Node start = new Node(coords[i].x, coords[i].y);   // (lon, lat)
                    Node end   = new Node(coords[i + 1].x, coords[i + 1].y);

                    double distKm = GeoUtils.haversine(start, end);

                    double denominator = (speed / 60.0 / typeFactor);
                    if (denominator == 0) denominator = 1e-6;
                    double weight = distKm / denominator;

                    addEdge(graph, start, end, weight);
                    if (!"yes".equals(oneway)) {
                        addEdge(graph, end, start, weight);
                    }
                }
            }
        } finally {
            dataStore.dispose();
        }

        return graph;
    }

    private static void addEdge(Map<Node, List<Edge>> graph, Node from, Node to, double weight) {
        List<Edge> edges = graph.get(from);
        if (edges == null) {
            edges = new ArrayList<Edge>();
            graph.put(from, edges);
        }
        edges.add(new Edge(to, weight));
    }

    private static String toLowerStr(Object value, String defaultVal) {
        if (value == null) return defaultVal;
        return String.valueOf(value).toLowerCase(Locale.ROOT);
    }

    private static double parseSpeed(Object value) {
        if (value == null) return 60.0;
        try {
            return Double.parseDouble(String.valueOf(value));
        } catch (NumberFormatException e) {
            return 60.0;
        }
    }
}
