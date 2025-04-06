var map = L.map("map").setView([38.952, -95.255], 12);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

var marker1 = L.marker([38.9416, -95.2436]).addTo(map);
marker1
  .bindPopup(
    `<a href="/dashboard/1">Douglas County Clerk and Elections Office</a>`,
  )
  .openPopup();

var marker2 = L.marker([38.9636, -95.2355]).addTo(map);
marker2.bindPopup(
  `<a href="/dashboard/2">Douglas County Courthouse
</a>`,
);
