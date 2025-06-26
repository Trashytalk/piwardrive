export default function DBStats({ metrics }) {
  const text = metrics?.db_stats || 'N/A';
  return <div>DB: {text}</div>;
}
