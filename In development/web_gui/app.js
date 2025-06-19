async function updateWidgets() {
    const widgets = document.getElementById('widgets');
    if (!widgets) return;
    const gps = await fetch('/api/gps').then(r => r.json());
    widgets.innerHTML = `
        <div class="card">Lat: ${gps.lat ?? 'N/A'}</div>
        <div class="card">Lon: ${gps.lon ?? 'N/A'}</div>
    `;
}

async function initMap() {
    const mapEl = document.getElementById('map');
    if (!mapEl) return;
    const map = new maplibregl.Map({
        container: 'map',
        style: 'https://demotiles.maplibre.org/style.json',
        center: [0, 0],
        zoom: 1,
    });
    const aps = await fetch('/api/aps').then(r => r.json());
    map.on('load', () => {
        map.addSource('aps', { type: 'geojson', data: aps });
        map.addLayer({ id: 'aps', type: 'circle', source: 'aps' });
    });
}

updateWidgets();
initMap();
