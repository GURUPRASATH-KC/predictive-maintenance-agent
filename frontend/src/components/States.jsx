import { Loader2, Inbox } from 'lucide-react'

export function Loading({ label = 'Loading...' }) {
  return (
    <div className="flex items-center justify-center gap-2 py-12 text-slate-500">
      <Loader2 className="w-4 h-4 animate-spin" />
      <span className="text-sm">{label}</span>
    </div>
  )
}

export function Empty({ label = 'Nothing here yet.' }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-12 text-slate-600">
      <Inbox className="w-6 h-6" />
      <span className="text-sm">{label}</span>
    </div>
  )
}

export function ErrorState({ message = 'Something went wrong.' }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-12 text-accent-red">
      <span className="text-sm">{message}</span>
    </div>
  )
}
