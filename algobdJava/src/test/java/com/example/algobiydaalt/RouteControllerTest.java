package com.example.algobiydaalt.controller;

import com.example.algobiydaalt.algorithms.*;
import com.example.algobiydaalt.graph.GraphBuilder;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.locationtech.jts.geom.Coordinate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import java.util.*;

@WebMvcTest(RouteController.class)
public class RouteControllerTest {

    @Autowired
    private MockMvc mvc;

    @BeforeAll
    static void setupMockGraph() throws Exception {
        var A = new Coordinate(0,0);
        var B = new Coordinate(1,0);

        Map<Coordinate, List<GraphBuilder.Edge>> mockGraph = new HashMap<>();
        mockGraph.put(A, List.of(new GraphBuilder.Edge(B, 1)));
        mockGraph.put(B, List.of());

        var fieldGraph = RouteController.class.getDeclaredField("graph");
        var fieldNodes = RouteController.class.getDeclaredField("nodes");
        fieldGraph.setAccessible(true);
        fieldNodes.setAccessible(true);

        fieldGraph.set(null, mockGraph);
        fieldNodes.set(null, new ArrayList<>(mockGraph.keySet()));
    }

    @Test
    void testRouteAPI() throws Exception {
        mvc.perform(get("/route")
                        .param("start", "0,0")
                        .param("end", "1,0")
                        .param("algo", "bfs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.algorithm").value("bfs"))
                .andExpect(jsonPath("$.path_length").value(2));
    }
}
