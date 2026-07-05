const colorMap = {
  blue: { bg: 'bg-accent-blue/15', text: 'text-accent-blue' },
  green: { bg: 'bg-accent-green/15', text: 'text-accent-green' },
  amber: { bg: 'bg-accent-amber/15', text: 'text-accent-amber' },
  red: { bg: 'bg-accent-red/15', text: 'text-accent-red' },
  purple: { bg: 'bg-accent-purple/15', text: 'text-accent-purple' },
}

export default function StatCard({ icon: Icon, label, value, sublabel, color = 'blue' }) {
  const c = colorMap[color] || colorMap.blue
  return (
    <div className="card p-4 flex flex-col gap-3">
      <div className="flex items-center gap-3">
        <div className={`w-9 h-9 rounded-lg ${c.bg} flex items-center justify-center`}>
          <Icon className={`w-4.5 h-4.5 ${c.text}`} style={{ width: 18, height: 18 }} />
        </div>
        <p className="text-sm text-slate-400 font-medium">{label}</p>
      </div>
      <div>
        <p className="text-2xl font-bold text-white leading-none">{value}</p>
        {sublabel && <p className={`text-xs mt-1.5 ${c.text}`}>{sublabel}</p>}
      </div>
    </div>
  )
}
