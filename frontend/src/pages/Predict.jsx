import { useEffect, useState } from 'react'
import { Gauge, Activity } from 'lucide-react'
import Navbar from '../layout/Navbar'
import RiskBadge from '../components/RiskBadge'
import AIRecommendationCard from '../components/AIRecommendationCard'
import { getEquipmentList } from '../api/equipment'
import { runPrediction } from '../api/predictions'

const initialForm = { equipment_id: '', temperature: '', vibration: '', pressure: '', rpm: '', load: '' }

export default function Predict() {
  const [equipmentList, setEquipmentList] = useState([])
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    getEquipmentList().then(setEquipmentList).catch(() => {})
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const data = await runPrediction({
        equipment_id: form.equipment_id,
        temperature: parseFloat(form.temperature),
        vibration: parseFloat(form.vibration),
        pressure: parseFloat(form.pressure),
        rpm: form.rpm ? parseFloat(form.rpm) : null,
        load: form.load ? parseFloat(form.load) : null,
        save_reading: true,
      })
      setResult(data)
    } catch (err) {
      setError('Prediction failed. Check the backend is running and equipment ID exists.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Navbar title="Predict Failure" subtitle="Enter live electrical asset sensor values to assess health and risk." />
      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-5">
            <Gauge className="w-4 h-4 text-accent-blue" />
            <p className="text-sm font-semibold text-white">Power Asset Sensor Input</p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1.5">Equipment</label>
              <select
                required
                value={form.equipment_id}
                onChange={(e) => setForm({ ...form, equipment_id: e.target.value })}
                className="w-full bg-surface-panel border border-surface-border rounded-lg px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-accent-blue"
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
              <NumField label="Temperature (°C)" value={form.temperature} onChange={(v) => setForm({ ...form, temperature: v })} />
              <NumField label="Vibration" value={form.vibration} onChange={(v) => setForm({ ...form, vibration: v })} />
              <NumField label="Pressure" value={form.pressure} onChange={(v) => setForm({ ...form, pressure: v })} />
              <NumField label="RPM (optional)" value={form.rpm} onChange={(v) => setForm({ ...form, rpm: v })} required={false} />
            </div>
            <NumField label="Load % (optional)" value={form.load} onChange={(v) => setForm({ ...form, load: v })} required={false} />
            <p className="text-xs text-slate-500">Use realistic electrical asset values such as transformer oil temperature, breaker contact temperature, or motor stator temperature.</p>

            {error && <p className="text-xs text-accent-red">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-lg bg-accent-blue text-white text-sm font-semibold hover:bg-accent-blue/90 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <Activity className="w-4 h-4" />
              {loading ? 'Predicting...' : 'Predict Failure'}
            </button>
          </form>
        </div>

        <div className="space-y-5">
          {!result && (
            <div className="card p-6 flex items-center justify-center h-full min-h-[240px] text-slate-600 text-sm">
              Select an asset and submit sensor values to view a power-system health assessment here.
            </div>
          )}

          {result && (
            <>
              <div className="card p-6">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-sm font-semibold text-white">Prediction Result</p>
                  <RiskBadge level={result.risk_level} />
                </div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <Metric label="Health Score" value={`${result.health_score}/100`} />
                  <Metric label="Failure Probability" value={`${result.failure_probability}%`} />
                </div>
                <p className="text-sm text-slate-400 bg-surface-panel/60 rounded-lg p-3 border border-surface-border">
                  {result.message}
                </p>
              </div>

              <AIRecommendationCard recommendation={result.ai_recommendation} />
            </>
          )}
        </div>
      </div>
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
        className="w-full bg-surface-panel border border-surface-border rounded-lg px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-accent-blue"
      />
    </div>
  )
}

function Metric({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-500 mb-1">{label}</p>
      <p className="text-xl font-bold text-white">{value}</p>
    </div>
  )
}
