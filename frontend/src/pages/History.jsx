import { useEffect, useState } from 'react'
import Navbar from '../layout/Navbar'
import RiskBadge from '../components/RiskBadge'
import { Loading, Empty, ErrorState } from '../components/States'
import { getPredictions } from '../api/predictions'

export default function History() {
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('All')

  useEffect(() => {
    getPredictions(200)
      .then(setPredictions)
      .catch(() => setError('Could not load prediction history. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  const filtered = filter === 'All' ? predictions : predictions.filter((p) => p.risk_level === filter)

  return (
    <div>
      <Navbar title="Prediction History" subtitle="Historical predictions and maintenance recommendations for power-system assets." />
      <div className="p-6 space-y-4">
        <div className="flex gap-2">
          {['All', 'Normal', 'Warning', 'Critical'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                filter === f
                  ? 'bg-accent-blue/15 border-accent-blue/40 text-accent-blue'
                  : 'border-surface-border text-slate-400 hover:text-slate-200'
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        {loading && <Loading label="Loading prediction history..." />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <div className="card overflow-hidden">
            {filtered.length === 0 ? (
              <Empty label="No predictions match this filter." />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs text-slate-500 border-b border-surface-border bg-surface-panel/40">
                      <th className="py-3 px-4 font-medium">Time</th>
                      <th className="py-3 px-4 font-medium">Equipment</th>
                      <th className="py-3 px-4 font-medium">Risk Level</th>
                      <th className="py-3 px-4 font-medium">Failure %</th>
                      <th className="py-3 px-4 font-medium">Recommendation Summary</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((p) => (
                      <tr key={p.id} className="border-b border-surface-border/50 last:border-0 hover:bg-white/[0.02]">
                        <td className="py-3 px-4 text-slate-500 text-xs whitespace-nowrap">
                          {new Date(p.created_at).toLocaleString()}
                        </td>
                        <td className="py-3 px-4 text-slate-200 font-medium">{p.equipment_name || p.equipment_id}</td>
                        <td className="py-3 px-4"><RiskBadge level={p.risk_level} /></td>
                        <td className="py-3 px-4 text-slate-300">{p.failure_probability}%</td>
                        <td className="py-3 px-4 text-slate-400 max-w-xs truncate">
                          {p.ai_recommendation?.possible_issue || '-'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
