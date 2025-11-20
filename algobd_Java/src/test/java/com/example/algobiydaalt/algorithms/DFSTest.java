package com.example.algobiydaalt.algorithms;

import com.example.algobiydaalt.graph.GraphBuilder;
import org.junit.jupiter.api.Test;
import org.locationtech.jts.geom.Coordinate;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class DFSTest {

    @Test
    void testDFS() {
        Coordinate A = new Coordinate(0,0);
        Coordinate B = new Coordinate(1,0);
        Coordinate C = new Coordinate(2,0);

        Map<Coordinate, List<GraphBuilder.Edge>> graph = new HashMap<>();
        graph.put(A, List.of(new GraphBuilder.Edge(B, 1)));
        graph.put(B, List.of(new GraphBuilder.Edge(C, 1)));
        graph.put(C, List.of());

        List<Coordinate> path = DFS.path(graph, A, C);

        assertEquals(3, path.size());
        assertEquals(A, path.get(0));
        assertEquals(B, path.get(1));
        assertEquals(C, path.get(2));
    }
}
