var map = L.map('map', {
    center: [-23.735422359974557, -46.58157182583245],
    zoom: 19
});
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxNativeZoom: 19,
    maxZoom: 19
}).addTo(map);