import { useState } from 'react';

const TEMPLATES = [
  { name: 'daily', label: 'Daily Summary' },
  { name: 'suspicious', label: 'Suspicious Activity' },
];

const SECTIONS = ['Summary', 'Charts', 'Tables'];

export default function ReportGenerator() {
  const [template, setTemplate] = useState('daily');
  const [sections, setSections] = useState([...SECTIONS]);
  const [schedule, setSchedule] = useState('none');
  const [preview, setPreview] = useState('');
  const [email, setEmail] = useState('');

  const move = (from, to) => {
    setSections((s) => {
      const arr = [...s];
      const [it] = arr.splice(from, 1);
      arr.splice(to, 0, it);
      return arr;
    });
  };

  const generate = async () => {
    const body = { template, sections, schedule };
    const resp = await fetch('/reports/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    setPreview(await resp.text());
  };

  const sendEmail = async () => {
    await fetch('/reports/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ template, to: email }),
    });
  };

  return (
    <div>
      <h3>Report Generator</h3>
      <select value={template} onChange={(e) => setTemplate(e.target.value)}>
        {TEMPLATES.map((t) => (
          <option key={t.name} value={t.name}>
            {t.label}
          </option>
        ))}
      </select>
      <div>
        {sections.map((s, idx) => (
          <div
            key={s}
            draggable
            onDragStart={(e) => e.dataTransfer.setData('idx', idx)}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              move(parseInt(e.dataTransfer.getData('idx'), 10), idx);
            }}
          >
            {s}
          </div>
        ))}
      </div>
      <select value={schedule} onChange={(e) => setSchedule(e.target.value)}>
        <option value="none">Manual</option>
        <option value="daily">Daily</option>
        <option value="weekly">Weekly</option>
      </select>
      <button onClick={generate}>Generate</button>
      <input
        type="email"
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={sendEmail}>Send</button>
      {preview && <pre className="report">{preview}</pre>}
    </div>
  );
}
