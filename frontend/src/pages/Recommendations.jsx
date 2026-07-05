import { useEffect, useState } from 'react'
import { Sparkles } from 'lucide-react'
import Navbar from '../layout/Navbar'
import AIRecommendationCard from '../components/AIRecommendationCard'
import { getEquipmentList } from '../api/equipment'
import { getAIRecommendation } from '../api/predictions'

const initialForm = { equipment_id: '', temperature: '', vibration: '', pressure: '' }

export default function Recommendations() {
  const [equipmentList, setEquipmentList] = useState([])
  const [form, setForm] = useState(initialForm)
  const [recommendation, setRecommendation] = useState(null)
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
      const data = await getAIRecommendation({
        equipment_id: form.equipment_id,
        temperature: parseFloat(form.temperature),
        vibration: parseFloat(form.vibration),
        pressure: parseFloat(form.pressure),
      })
      setRecommendation(data)
    } catch (err) {
      setError('Could not generate a recommendation. Check the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Navbar title="AI Recommendations" subtitle="Get electrical asset maintenance guidance based on sensor inputs and health scoring." />
      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-5">
            <Sparkles className="w-4 h-4 text-accent-purple" />
            <p className="text-sm font-semibold text-white">Ask the Power Asset Agent</p>
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
            <div className="grid grid-cols-3 gap-3">
              <NumField label="Temperature" value={form.temperature} onChange={(v) => setForm({ ...form, temperature: v })} />
              <NumField label="Vibration" value={form.vibration} onChange={(v) => setForm({ ...form, vibration: v })} />
              <NumField label="Pressure" value={form.pressure} onChange={(v) => setForm({ ...form, pressure: v })} />
            </div>

            {error && <p className="text-xs text-accent-red">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-lg bg-accent-purple text-white text-sm font-semibold hover:bg-accent-purple/90 disabled:opacity-50"
            >
              {loading ? 'Thinking...' : 'Get Recommendation'}
            </button>
          </form>
        </div>

        <div>
          {!recommendation ? (
            <div className="card p-6 flex items-center justify-center h-full min-h-[240px] text-slate-600 text-sm">
              Power-system maintenance recommendations will appear here.
            </div>
          ) : (
            <AIRecommendationCard recommendation={recommendation} />
          )}
        </div>
      </div>
    </div>
  )
}

function NumField({ label, value, onChange }) {
  return (
    <div>
      <label className="block text-xs text-slate-400 mb-1.5">{label}</label>
      <input
        type="number"
        step="any"
        required
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-surface-panel border border-surface-border rounded-lg px-3 py-2.5 text-sm text-slate-200 outline-none focus:border-accent-blue"
      />
    </div>
  )
}
