const map = L.map("map").setView([47.92, 106.92], 12);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

let points = [];
let routeLayer = null;
let markers = [];
const algorithmSelect = document.getElementById("algorithm");
const clearBtn = document.getElementById("clear");

function drawRoute(coords) {
  if (routeLayer) map.removeLayer(routeLayer);
  routeLayer = L.polyline(coords, { color: "red", weight: 4 }).addTo(map);
  map.fitBounds(routeLayer.getBounds());
}

function requestRoute() {
  if (points.length === 2) {
    const algo = algorithmSelect.value;
    const [start, end] = points;
    fetch(`http://127.0.0.1:5000/route?start=${start}&end=${end}&algo=${algo}`)
      .then(res => res.json())
      .then(data => {
        if (data.path?.length) {
          const coords = data.path.map(([x, y]) => [y, x]);
          drawRoute(coords);
          console.log(`${algo.toUpperCase()} Runtime: ${data.runtime_seconds}s, Memory: ${data.memory_mb}MB`);
        } else {
          alert("No path found!");
        }
      })
      .catch(() => alert("Error fetching route!"));
  }
}

map.on("click", (e) => {
  const { lat, lng } = e.latlng;
  if (points.length < 2) {
    points.push([lng, lat]);
    const color = points.length === 1 ? "green" : "orange";
    const marker = L.circleMarker([lat, lng], {
      radius: 8,
      color,
      fillColor: color,
      fillOpacity: 0.8
    }).addTo(map);
    markers.push(marker);
  }
  if (points.length === 2) requestRoute();
});

algorithmSelect.addEventListener("change", () => {
  if (points.length === 2) requestRoute();
});

clearBtn.addEventListener("click", () => {
  points = [];
  markers.forEach(m => map.removeLayer(m));
  markers = [];
  if (routeLayer) map.removeLayer(routeLayer);
});
