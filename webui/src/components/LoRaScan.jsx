export default function LoRaScan({ metrics }) {
  const count = metrics?.lora_devices;
  return <div>LoRa: {count != null ? count : 'N/A'}</div>;
}
