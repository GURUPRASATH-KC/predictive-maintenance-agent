import { useEffect, useState } from 'react'
import { Plus, Pencil, Trash2, X } from 'lucide-react'
import Navbar from '../layout/Navbar'
import RiskBadge from '../components/RiskBadge'
import { Loading, Empty, ErrorState } from '../components/States'
import { getEquipmentList, createEquipment, updateEquipment, deleteEquipment } from '../api/equipment'

const emptyForm = {
  equipment_id: '',
  equipment_name: '',
  equipment_type: '',
  location: '',
  installation_date: '',
}

export default function Equipment() {
  const [list, setList] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)

  async function load() {
    setLoading(true)
    try {
      const data = await getEquipmentList()
      setList(data)
      setError(null)
    } catch (err) {
      setError('Could not load equipment. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  function openCreate() {
    setForm(emptyForm)
    setEditingId(null)
    setShowForm(true)
  }

  function openEdit(eq) {
    setForm({
      equipment_id: eq.equipment_id,
      equipment_name: eq.equipment_name,
      equipment_type: eq.equipment_type,
      location: eq.location,
      installation_date: eq.installation_date,
    })
    setEditingId(eq.id)
    setShowForm(true)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    try {
      if (editingId) {
        await updateEquipment(editingId, form)
      } else {
        await createEquipment(form)
      }
      setShowForm(false)
      await load()
    } catch (err) {
      alert(err?.response?.data?.detail || 'Failed to save equipment')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(id) {
    if (!confirm('Delete this equipment? This cannot be undone.')) return
    try {
      await deleteEquipment(id)
      await load()
    } catch (err) {
      alert('Failed to delete equipment')
    }
  }

  return (
    <div>
      <Navbar title="Equipment" subtitle="Manage critical power-system assets and their monitoring status." />
      <div className="p-6 space-y-4">
        <div className="flex justify-end">
          <button
            onClick={openCreate}
            className="flex items-center gap-2 bg-accent-blue hover:bg-accent-blue/90 text-white text-sm font-medium px-4 py-2.5 rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" /> Add Equipment
          </button>
        </div>

        {loading && <Loading label="Loading equipment..." />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <div className="card overflow-hidden">
            {list.length === 0 ? (
              <Empty label="No equipment added yet." />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs text-slate-500 border-b border-surface-border bg-surface-panel/40">
                      <th className="py-3 px-4 font-medium">ID</th>
                      <th className="py-3 px-4 font-medium">Name</th>
                      <th className="py-3 px-4 font-medium">Type</th>
                      <th className="py-3 px-4 font-medium">Location</th>
                      <th className="py-3 px-4 font-medium">Installed</th>
                      <th className="py-3 px-4 font-medium">Status</th>
                      <th className="py-3 px-4 font-medium text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {list.map((eq) => (
                      <tr key={eq.id} className="border-b border-surface-border/50 last:border-0 hover:bg-white/[0.02]">
                        <td className="py-3 px-4 text-slate-400 font-mono text-xs">{eq.equipment_id}</td>
                        <td className="py-3 px-4 text-slate-200 font-medium">{eq.equipment_name}</td>
                        <td className="py-3 px-4 text-slate-400">{eq.equipment_type}</td>
                        <td className="py-3 px-4 text-slate-400">{eq.location}</td>
                        <td className="py-3 px-4 text-slate-400">{eq.installation_date}</td>
                        <td className="py-3 px-4"><RiskBadge level={eq.status} /></td>
                        <td className="py-3 px-4">
                          <div className="flex justify-end gap-2">
                            <button onClick={() => openEdit(eq)} className="w-8 h-8 rounded-lg border border-surface-border flex items-center justify-center text-slate-400 hover:text-accent-blue hover:border-accent-blue/40">
                              <Pencil className="w-3.5 h-3.5" />
                            </button>
                            <button onClick={() => handleDelete(eq.id)} className="w-8 h-8 rounded-lg border border-surface-border flex items-center justify-center text-slate-400 hover:text-accent-red hover:border-accent-red/40">
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
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

      {showForm && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="card w-full max-w-md p-6">
            <div className="flex items-center justify-between mb-5">
              <p className="text-base font-semibold text-white">
                {editingId ? 'Edit Asset' : 'Add Asset'}
              </p>
              <button onClick={() => setShowForm(false)} className="text-slate-500 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-3">
              <Field label="Equipment ID" required disabled={!!editingId} value={form.equipment_id}
                onChange={(v) => setForm({ ...form, equipment_id: v })} placeholder="EQ005" />
              <Field label="Equipment Name" required value={form.equipment_name}
                onChange={(v) => setForm({ ...form, equipment_name: v })} placeholder="Motor E" />
              <Field label="Equipment Type" required value={form.equipment_type}
                onChange={(v) => setForm({ ...form, equipment_type: v })} placeholder="Motor" />
              <Field label="Location" required value={form.location}
                onChange={(v) => setForm({ ...form, location: v })} placeholder="Plant Floor 1" />
              <Field label="Installation Date" required type="date" value={form.installation_date}
                onChange={(v) => setForm({ ...form, installation_date: v })} />

              <div className="flex gap-2 pt-2">
                <button type="button" onClick={() => setShowForm(false)}
                  className="flex-1 py-2.5 rounded-lg border border-surface-border text-slate-300 text-sm font-medium hover:bg-white/5">
                  Cancel
                </button>
                <button type="submit" disabled={saving}
                  className="flex-1 py-2.5 rounded-lg bg-accent-blue text-white text-sm font-medium hover:bg-accent-blue/90 disabled:opacity-50">
                  {saving ? 'Saving...' : 'Save'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

function Field({ label, value, onChange, placeholder, type = 'text', required, disabled }) {
  return (
    <div>
      <label className="block text-xs text-slate-400 mb-1.5">{label}</label>
      <input
        type={type}
        required={required}
        disabled={disabled}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-surface-panel border border-surface-border rounded-lg px-3 py-2 text-sm text-slate-200 outline-none focus:border-accent-blue disabled:opacity-50"
      />
    </div>
  )
}
