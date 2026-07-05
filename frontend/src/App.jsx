import { Routes, Route } from 'react-router-dom'
import Sidebar from './layout/Sidebar'
import Dashboard from './pages/Dashboard'
import Equipment from './pages/Equipment'
import Sensors from './pages/Sensors'
import Predict from './pages/Predict'
import History from './pages/History'
import Recommendations from './pages/Recommendations'

export default function App() {
  return (
    <div className="flex min-h-screen bg-surface text-slate-200">
      <Sidebar />
      <main className="flex-1 min-w-0">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/equipment" element={<Equipment />} />
          <Route path="/sensors" element={<Sensors />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/history" element={<History />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </main>
    </div>
  )
}
