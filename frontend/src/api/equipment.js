import client from './client'

export const getEquipmentList = () => client.get('/api/equipment').then((r) => r.data)
export const getEquipment = (id) => client.get(`/api/equipment/${id}`).then((r) => r.data)
export const createEquipment = (data) => client.post('/api/equipment', data).then((r) => r.data)
export const updateEquipment = (id, data) => client.put(`/api/equipment/${id}`, data).then((r) => r.data)
export const deleteEquipment = (id) => client.delete(`/api/equipment/${id}`).then((r) => r.data)
