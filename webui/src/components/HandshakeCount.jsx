export default function HandshakeCount({ metrics }) {
  return <div>Handshakes: {metrics?.handshake_count ?? 'N/A'}</div>;
}
