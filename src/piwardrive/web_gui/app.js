async function updateWidgets() {
    const container = document.getElementById('widgets');
    if (!container) return;

    const [gps, names] = await Promise.all([
        fetch('/api/gps').then(r => r.json()),
        fetch('/api/widgets').then(r => r.json()),
    ]);

    container.innerHTML = '';
    const header = document.createElement('div');
    header.className = 'mb-2 font-bold';
    header.textContent = `Lat: ${gps.lat ?? 'N/A'}  Lon: ${gps.lon ?? 'N/A'}`;
    container.appendChild(header);

    const list = document.createElement('ul');
    list.className = 'list-disc pl-5';
    for (const name of names) {
        const li = document.createElement('li');
        li.textContent = name;
        list.appendChild(li);
    }
    container.appendChild(list);
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
