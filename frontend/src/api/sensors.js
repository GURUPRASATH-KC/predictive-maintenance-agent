import client from './client'

export const getSensorReadings = (limit = 100) =>
  client.get('/api/sensors', { params: { limit } }).then((r) => r.data)

export const getSensorReadingsForEquipment = (equipmentId, limit = 100) =>
  client.get(`/api/sensors/equipment/${equipmentId}`, { params: { limit } }).then((r) => r.data)

export const createSensorReading = (data) => client.post('/api/sensors', data).then((r) => r.data)
