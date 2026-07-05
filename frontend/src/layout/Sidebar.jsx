import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Boxes,
  Activity,
  Gauge,
  History,
  Sparkles,
  HeartPulse,
} from 'lucide-react'

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/equipment', label: 'Equipment', icon: Boxes },
  { to: '/sensors', label: 'Sensors', icon: Activity },
  { to: '/predict', label: 'Predict Failure', icon: Gauge },
  { to: '/history', label: 'History', icon: History },
  { to: '/recommendations', label: 'AI Recommendations', icon: Sparkles },
]

export default function Sidebar() {
  return (
    <aside className="hidden lg:flex flex-col w-64 shrink-0 bg-surface-panel border-r border-surface-border h-screen sticky top-0">
      <div className="flex items-center gap-2 px-5 h-16 border-b border-surface-border">
        <div className="w-9 h-9 rounded-lg bg-accent-blue/15 flex items-center justify-center">
          <HeartPulse className="w-5 h-5 text-accent-blue" />
        </div>
        <div>
          <p className="text-sm font-bold text-white leading-none">AI-Based Predictive Maintenance</p>
          <p className="text-[11px] text-accent-blue font-medium tracking-wide">POWER SYSTEM EQUIPMENT</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        <p className="px-3 text-[11px] font-semibold text-slate-500 tracking-wider mb-2">
          PLATFORM
        </p>
        {links.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-accent-blue/15 text-accent-blue'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`
            }
          >
            <Icon className="w-4 h-4" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-surface-border">
        <div className="rounded-xl bg-gradient-to-br from-accent-blue/15 to-accent-purple/10 border border-accent-blue/20 p-4">
          <p className="text-xs font-semibold text-white mb-1">AI Maintenance Agent</p>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Rule-based insights are generated automatically for every prediction.
          </p>
        </div>
      </div>
    </aside>
  )
}
