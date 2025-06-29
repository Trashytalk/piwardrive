import { useEffect, useRef, useState } from 'react';

export default function LogViewer({ path = '/var/log/syslog', lines = 200 }) {
  const [paths, setPaths] = useState([path]);
  const [curPath, setCurPath] = useState(path);
  const [text, setText] = useState('');
  const [filter, setFilter] = useState('');
  const preRef = useRef(null);

  // fetch list of allowed log paths once
  useEffect(() => {
    fetch('/config')
      .then(r => r.json())
      .then(cfg => {
        if (Array.isArray(cfg.log_paths) && cfg.log_paths.length) {
          setPaths(cfg.log_paths);
          if (!path) setCurPath(cfg.log_paths[0]);
        }
      })
      .catch(() => {});
  }, [path]);

  useEffect(() => {
    const load = () => {
      const params = new URLSearchParams({ path: curPath, lines });
      fetch(`/logs?${params}`)
        .then(r => r.json())
        .then(d => {
          let linesArr = d.lines || [];
          if (filter) {
            try {
              const re = new RegExp(filter);
              linesArr = linesArr.filter(ln => re.test(ln));
            } catch {
              // ignore invalid regex
            }
          }
          setText(linesArr.join('\n'));
        })
        .catch(() => setText(''));
    };
    load();
    const id = setInterval(load, 1000);
    return () => clearInterval(id);
  }, [curPath, lines, filter]);

  const jumpToError = () => {
    if (!preRef.current) return;
    try {
      const re = /error/i;
      const linesArr = text.split('\n');
      for (let i = linesArr.length - 1; i >= 0; i -= 1) {
        if (re.test(linesArr[i])) {
          const pos = (preRef.current.scrollHeight * i) / linesArr.length;
          preRef.current.scrollTop = pos;
          break;
        }
      }
    } catch {
      /* ignore */
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '0.5em' }}>
        <select value={curPath} onChange={e => setCurPath(e.target.value)}>
          {paths.map(p => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
        <input
          placeholder="Filter regex"
          value={filter}
          onChange={e => setFilter(e.target.value)}
          style={{ marginLeft: '0.5em' }}
        />
        <button onClick={jumpToError} style={{ marginLeft: '0.5em' }}>
          Last Error
        </button>
      </div>
      <pre ref={preRef} style={{ maxHeight: '200px', overflowY: 'scroll' }}>
        {text}
      </pre>
    </div>
  );
}
