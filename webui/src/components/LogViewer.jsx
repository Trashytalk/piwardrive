import { useEffect, useState } from 'react';

export default function LogViewer({ path = '/var/log/syslog', lines = 200 }) {
  const [text, setText] = useState('');

  useEffect(() => {
    const load = () => {
      const params = new URLSearchParams({ path, lines });
      fetch(`/logs?${params}`)
        .then(r => r.json())
        .then(d => setText(d.lines.join('\n')))
        .catch(() => setText(''));
    };
    load();
    const id = setInterval(load, 1000);
    return () => clearInterval(id);
  }, [path, lines]);

  return <pre style={{ maxHeight: '200px', overflowY: 'scroll' }}>{text}</pre>;
}
