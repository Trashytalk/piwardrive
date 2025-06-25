import { useState } from 'react';

export default function VectorTileCustomizer() {
  const [mbtiles, setMbtiles] = useState('');
  const [style, setStyle] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('');

  const submit = () => {
    fetch('/api/vector-tiles/style', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mbtiles, style, name, description }),
    })
      .then(r => r.json())
      .then(() => setStatus('Updated'))
      .catch(() => setStatus('Error'));
  };

  return (
    <section>
      <h2>Vector Tile Customizer</h2>
      <div>
        <label>
          MBTiles Path
          <input value={mbtiles} onChange={e => setMbtiles(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          Style JSON
          <textarea
            value={style}
            onChange={e => setStyle(e.target.value)}
            rows={4}
            cols={40}
          />
        </label>
      </div>
      <div>
        <label>
          Name
          <input value={name} onChange={e => setName(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          Description
          <input
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
        </label>
      </div>
      <button onClick={submit}>Apply</button>
      {status && <p>{status}</p>}
    </section>
  );
}
