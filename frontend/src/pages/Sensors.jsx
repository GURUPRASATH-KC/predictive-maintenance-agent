import { useEffect, useState } from 'react'
import { Plus, X } from 'lucide-react'
import Navbar from '../layout/Navbar'
import { Loading, Empty, ErrorState } from '../components/States'
import { getSensorReadings, createSensorReading } from '../api/sensors'
import { getEquipmentList } from '../api/equipment'

const emptyForm = { equipment_id: '', temperature: '', vibration: '', pressure: '', rpm: '', load: '' }

export default function Sensors() {
  const [readings, setReadings] = useState([])
  const [equipmentList, setEquipmentList] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)

  async function load() {
    setLoading(true)
    try {
      const [r, e] = await Promise.all([getSensorReadings(100), getEquipmentList()])
      setReadings(r)
      setEquipmentList(e)
      setError(null)
    } catch (err) {
      setError('Could not load sensor data. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    try {
      await createSensorReading({
        equipment_id: form.equipment_id,
        temperature: parseFloat(form.temperature),
        vibration: parseFloat(form.vibration),
        pressure: parseFloat(form.pressure),
        rpm: form.rpm ? parseFloat(form.rpm) : null,
        load: form.load ? parseFloat(form.load) : null,
      })
      setShowForm(false)
      setForm(emptyForm)
      await load()
    } catch (err) {
      alert('Failed to save sensor reading')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <Navbar title="Sensor Data" subtitle="Add and review sensor readings for transformers, breakers, generators, motors, switchgear, and capacitor banks." />
      <div className="p-6 space-y-4">
        <div className="flex justify-end">
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 bg-accent-blue hover:bg-accent-blue/90 text-white text-sm font-medium px-4 py-2.5 rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" /> Add Reading
          </button>
        </div>

        {loading && <Loading label="Loading sensor readings..." />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <div className="card overflow-hidden">
            {readings.length === 0 ? (
              <Empty label="No sensor readings recorded yet." />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs text-slate-500 border-b border-surface-border bg-surface-panel/40">
                      <th className="py-3 px-4 font-medium">Equipment ID</th>
                      <th className="py-3 px-4 font-medium">Temp (°C)</th>
                      <th className="py-3 px-4 font-medium">Vibration (mm/s)</th>
                      <th className="py-3 px-4 font-medium">Pressure</th>
                      <th className="py-3 px-4 font-medium">RPM</th>
                      <th className="py-3 px-4 font-medium">Load</th>
                      <th className="py-3 px-4 font-medium">Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {readings.map((r) => (
                      <tr key={r.id} className="border-b border-surface-border/50 last:border-0 hover:bg-white/[0.02]">
                        <td className="py-3 px-4 text-slate-200 font-mono text-xs">{r.equipment_id}</td>
                        <td className="py-3 px-4 text-slate-300">{r.temperature}</td>
                        <td className="py-3 px-4 text-slate-300">{r.vibration}</td>
                        <td className="py-3 px-4 text-slate-300">{r.pressure}</td>
                        <td className="py-3 px-4 text-slate-400">{r.rpm ?? '-'}</td>
                        <td className="py-3 px-4 text-slate-400">{r.load ?? '-'}</td>
                        <td className="py-3 px-4 text-slate-500 text-xs">{new Date(r.timestamp).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="card w-full max-w-md p-6">
            <div className="flex items-center justify-between mb-5">
              <p className="text-base font-semibold text-white">Add Sensor Reading</p>
              <button onClick={() => setShowForm(false)} className="text-slate-500 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1.5">Equipment</label>
                <select
                  required
                  value={form.equipment_id}
                  onChange={(e) => setForm({ ...form, equipment_id: e.target.value })}
                  className="w-full bg-surface-panel border border-surface-border rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-accent-blue"
                >
                  <option value="">Select equipment</option>
                  {equipmentList.map((eq) => (
                    <option key={eq.id} value={eq.equipment_id}>
                      {eq.equipment_name} ({eq.equipment_id})
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <NumField label="Temperature" value={form.temperature} onChange={(v) => setForm({ ...form, temperature: v })} />
                <NumField label="Vibration" value={form.vibration} onChange={(v) => setForm({ ...form, vibration: v })} />
                <NumField label="Pressure" value={form.pressure} onChange={(v) => setForm({ ...form, pressure: v })} />
                <NumField label="RPM (optional)" value={form.rpm} onChange={(v) => setForm({ ...form, rpm: v })} required={false} />
              </div>
              <NumField label="Load % (optional)" value={form.load} onChange={(v) => setForm({ ...form, load: v })} required={false} />

              <div className="flex gap-2 pt-2">
                <button type="button" onClick={() => setShowForm(false)}
                  className="flex-1 py-2.5 rounded-lg border border-surface-border text-slate-300 text-sm font-medium hover:bg-white/5">
                  Cancel
                </button>
                <button type="submit" disabled={saving}
                  className="flex-1 py-2.5 rounded-lg bg-accent-blue text-white text-sm font-medium hover:bg-accent-blue/90 disabled:opacity-50">
                  {saving ? 'Saving...' : 'Save Reading'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

function NumField({ label, value, onChange, required = true }) {
  return (
    <div>
      <label className="block text-xs text-slate-400 mb-1.5">{label}</label>
      <input
        type="number"
        step="any"
        required={required}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-surface-panel border border-surface-border rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-accent-blue"
      />
    </div>
  )
}
