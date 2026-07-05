import { Sparkles, AlertTriangle, Wrench, Clock } from 'lucide-react'

const urgencyColor = {
  Low: 'text-accent-green bg-accent-green/10 border-accent-green/30',
  Medium: 'text-accent-amber bg-accent-amber/10 border-accent-amber/30',
  High: 'text-accent-red bg-accent-red/10 border-accent-red/30',
}

export default function AIRecommendationCard({ recommendation }) {
  if (!recommendation) return null
  const { possible_issue, reason, recommended_action, urgency, inspection_window } = recommendation

  return (
    <div className="card p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent-purple/15 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-accent-purple" />
          </div>
          <p className="text-sm font-semibold text-white">AI Maintenance Advice</p>
        </div>
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-md border ${urgencyColor[urgency] || urgencyColor.Medium}`}>
          {urgency} urgency
        </span>
      </div>

      <div className="flex items-start gap-2">
        <AlertTriangle className="w-4 h-4 text-accent-amber mt-0.5 shrink-0" />
        <div>
          <p className="text-sm text-white font-medium">{possible_issue}</p>
          <p className="text-xs text-slate-500 mt-0.5">{reason}</p>
        </div>
      </div>

      <div className="flex items-start gap-2">
        <Wrench className="w-4 h-4 text-accent-blue mt-0.5 shrink-0" />
        <div className="flex-1">
          <p className="text-xs text-slate-400 mb-1.5">Recommended actions</p>
          <ul className="space-y-1">
            {recommended_action?.map((action, i) => (
              <li key={i} className="text-sm text-slate-300 flex items-start gap-1.5">
                <span className="text-accent-blue mt-1.5 w-1 h-1 rounded-full bg-accent-blue shrink-0" />
                {action}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="flex items-center gap-2 pt-1 border-t border-surface-border">
        <Clock className="w-4 h-4 text-slate-500" />
        <p className="text-xs text-slate-400">
          Inspect: <span className="text-slate-200 font-medium">{inspection_window}</span>
        </p>
      </div>
    </div>
  )
}
