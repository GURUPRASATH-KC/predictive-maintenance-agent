import { Search, Bell } from 'lucide-react'
import ThemeToggle from '../components/ThemeToggle'

export default function Navbar({ title, subtitle }) {
  return (
    <header className="sticky top-0 z-10 h-16 flex items-center justify-between px-6 bg-surface/80 backdrop-blur border-b border-surface-border">
      <div>
        <h1 className="text-white font-semibold text-lg leading-none">{title}</h1>
        {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden md:flex items-center gap-2 bg-surface-card border border-surface-border rounded-lg px-3 py-2 w-72">
          <Search className="w-4 h-4 text-slate-500" />
          <input
            placeholder="Search equipment, predictions..."
            className="bg-transparent text-sm text-slate-300 placeholder:text-slate-600 outline-none w-full"
          />
        </div>
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <button className="relative w-9 h-9 rounded-lg bg-surface-card border border-surface-border flex items-center justify-center text-slate-400 hover:text-white">
            <Bell className="w-4 h-4" />
          </button>
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-accent-blue to-accent-purple flex items-center justify-center text-white text-sm font-semibold">
            A
          </div>
        </div>
      </div>
    </header>
  )
}
