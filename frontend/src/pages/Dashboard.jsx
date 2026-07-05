import { useEffect, useState } from 'react'
import { Boxes, ShieldCheck, AlertTriangle, ShieldAlert, Gauge } from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import Navbar from '../layout/Navbar'
import StatCard from '../components/StatCard'
import RiskBadge from '../components/RiskBadge'
import { Loading, ErrorState } from '../components/States'
import { getDashboardSummary, getRecentPredictions, getRiskDistribution } from '../api/predictions'
import { getEquipmentList } from '../api/equipment'

const COLORS = { Normal: '#10B981', Warning: '#F59E0B', Critical: '#EF4444' }

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [recent, setRecent] = useState([])
  const [distribution, setDistribution] = useState(null)
  const [equipment, setEquipment] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const [s, r, d, e] = await Promise.all([
          getDashboardSummary(),
          getRecentPredictions(5),
          getRiskDistribution(),
          getEquipmentList(),
        ])
        setSummary(s)
        setRecent(r)
        setDistribution(d)
        setEquipment(e)
      } catch (err) {
        setError('Could not reach the backend API. Make sure it is running on the configured URL.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const pieData = distribution
    ? distribution.labels.map((label, i) => ({ name: label, value: distribution.values[i] }))
    : []

  return (
    <div>
      <Navbar title="Power System Asset Dashboard" subtitle="Real-time monitoring and health insights for transformers, breakers, generators, motors, switchgear, and capacitor banks." />
      <div className="p-6 space-y-6">
        {loading && <Loading label="Loading dashboard..." />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard icon={Boxes} label="Total Equipment" value={summary.total_equipment} color="blue" />
              <StatCard icon={ShieldCheck} label="Normal" value={summary.normal_count} color="green" sublabel={`${pct(summary.normal_count, summary.total_equipment)}% of assets`} />
              <StatCard icon={AlertTriangle} label="Warning" value={summary.warning_count} color="amber" sublabel={`${pct(summary.warning_count, summary.total_equipment)}% of assets`} />
              <StatCard icon={ShieldAlert} label="Critical" value={summary.critical_count} color="red" sublabel={`${pct(summary.critical_count, summary.total_equipment)}% of assets`} />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="card p-5 lg:col-span-1">
                <p className="text-sm font-semibold text-white mb-4">Asset Health Distribution</p>
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={80} paddingAngle={3}>
                        {pieData.map((entry) => (
                          <Cell key={entry.name} fill={COLORS[entry.name]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ background: '#151F35', border: '1px solid #22304A', borderRadius: 8, fontSize: 12 }} />
                      <Legend verticalAlign="middle" align="right" layout="vertical" iconType="circle" wrapperStyle={{ fontSize: 12, color: '#94A3B8' }} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="card p-5 lg:col-span-2">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-sm font-semibold text-white">Recent Asset Predictions</p>
                  <Gauge className="w-4 h-4 text-slate-500" />
                </div>
                {recent.length === 0 ? (
                  <p className="text-sm text-slate-500 py-8 text-center">No predictions yet. Run one from the Predict page.</p>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="text-left text-xs text-slate-500 border-b border-surface-border">
                          <th className="pb-2 font-medium">Equipment</th>
                          <th className="pb-2 font-medium">Health</th>
                          <th className="pb-2 font-medium">Risk</th>
                          <th className="pb-2 font-medium">Failure %</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recent.map((p) => (
                          <tr key={p.id} className="border-b border-surface-border/50 last:border-0">
                            <td className="py-2.5 text-slate-200">{p.equipment_name || p.equipment_id}</td>
                            <td className="py-2.5 text-slate-300">{p.health_score}</td>
                            <td className="py-2.5"><RiskBadge level={p.risk_level} /></td>
                            <td className="py-2.5 text-slate-300">{p.failure_probability}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>

            <div className="card p-5">
              <p className="text-sm font-semibold text-white mb-4">Electrical Equipment Health Summary</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {equipment.map((eq) => (
                  <div key={eq.id} className="rounded-lg border border-surface-border p-3 bg-surface-panel/40">
                    <div className="flex items-center justify-between mb-1.5">
                      <p className="text-sm font-medium text-white">{eq.equipment_name}</p>
                      <RiskBadge level={eq.status} />
                    </div>
                    <p className="text-xs text-slate-500">{eq.equipment_type} · {eq.location}</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

function pct(count, total) {
  if (!total) return 0
  return Math.round((count / total) * 100)
}
