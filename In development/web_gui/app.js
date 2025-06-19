async function updateWidgets() {
    const widgets = document.getElementById('widgets');
    if (!widgets) return;
    const gps = await fetch('/api/gps').then(r => r.json());
    widgets.innerHTML = `
        <div class="p-2 bg-gray-100 rounded">Lat: ${gps.lat ?? 'N/A'}</div>
        <div class="p-2 bg-gray-100 rounded">Lon: ${gps.lon ?? 'N/A'}</div>
    `;
}

async function initMap() {
    const mapEl = document.getElementById('map');
    if (!mapEl) return;
    const map = new maplibregl.Map({
        container: 'map',
        style: {
            version: 8,
            sources: {
                offline: {
                    type: 'raster',
                    tiles: ['http://localhost:8080/services/offline/{z}/{x}/{y}.png'],
                    tileSize: 256
                }
            },
            layers: [{ id: 'offline', type: 'raster', source: 'offline' }]
        },
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
