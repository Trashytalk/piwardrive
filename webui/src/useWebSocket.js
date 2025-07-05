import { useEffect, useRef, useState } from 'react';

export function useWebSocket(
  url,
  { onMessage, buffer = false, protocols } = {}
) {
  const wsRef = useRef(null);
  const bufferRef = useRef([]);
  const [status, setStatus] = useState('connecting');

  useEffect(() => {
    let cancelled = false;
    let timer = null;

    function connect() {
      if (cancelled) return;
      setStatus('connecting');
      try {
        const ws = new WebSocket(url, protocols);
        wsRef.current = ws;
        ws.onopen = () => {
          setStatus('open');
          if (buffer && bufferRef.current.length) {
            bufferRef.current.forEach((msg) => ws.send(msg));
            bufferRef.current = [];
          }
        };
        ws.onmessage = (ev) => {
          if (onMessage) onMessage(ev.data);
        };
        ws.onclose = () => {
          if (cancelled) return;
          setStatus('closed');
          timer = setTimeout(connect, 3000);
        };
        ws.onerror = () => {
          ws.close();
        };
      } catch (_) {
        timer = setTimeout(connect, 3000);
      }
    }

    connect();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
      if (wsRef.current) wsRef.current.close();
    };
  }, [url, protocols, onMessage, buffer]);

  const send = (msg) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(msg);
    } else if (buffer) {
      bufferRef.current.push(msg);
    }
  };

  return { send, status };
}
