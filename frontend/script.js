const map = L.map("map").setView([47.92, 106.92], 12);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

let points = [];
let routeLayer = null;
let markers = [];

const algorithmSelect = document.getElementById("algorithm");
const clearBtn = document.getElementById("clear");

function drawRoute(coords) {
  // Remove previous route if exists
  if (routeLayer) {
    map.removeLayer(routeLayer);
  }

  // Draw new route line
  routeLayer = L.polyline(coords, { color: "red", weight: 4 }).addTo(map);
  map.fitBounds(routeLayer.getBounds());
}

function requestRoute() {
  if (points.length === 2) {
    const algo = algorithmSelect.value;
    const start = points[0];
    const end = points[1];

    fetch(`http://127.0.0.1:5000/route?start=${start}&end=${end}&algo=${algo}`)
      .then(res => res.json())
      .then(data => {
        if (data.path && data.path.length > 0) {
          const coords = data.path.map(([x, y]) => [y, x]);
          drawRoute(coords);

          console.log(`${algo.toUpperCase()} Runtime: ${data.runtime_seconds}s, Memory: ${data.memory_mb}MB`);
        } else {
          alert("No path found!");
        }
      })
      .catch(err => {
        console.error(err);
        alert("Error fetching route!");
      });
  }
}

// When user clicks map
map.on("click", (e) => {
  const { lat, lng } = e.latlng;

  // Limit to two points (start & end)
  if (points.length < 2) {
    points.push([lng, lat]);
    const markerColor = points.length === 1 ? "green" : "orange";
    const marker = L.circleMarker([lat, lng], {
      radius: 8,
      color: markerColor,
      fillColor: markerColor,
      fillOpacity: 0.8
    }).addTo(map);
    markers.push(marker);
  }

  // Automatically request route when 2 points are selected
  if (points.length === 2) {
    requestRoute();
  }
});

// Recalculate route when algorithm is changed
algorithmSelect.addEventListener("change", () => {
  if (points.length === 2) {
    requestRoute();
  }
});

// Clear map
clearBtn.addEventListener("click", () => {
  points = [];
  markers.forEach(m => map.removeLayer(m));
  markers = [];
  if (routeLayer) map.removeLayer(routeLayer);
});
