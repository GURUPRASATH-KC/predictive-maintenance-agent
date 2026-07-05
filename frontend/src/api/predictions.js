import client from './client'

export const runPrediction = (data) => client.post('/api/predict', data).then((r) => r.data)

export const getPredictions = (limit = 200) =>
  client.get('/api/predictions', { params: { limit } }).then((r) => r.data)

export const getPredictionsForEquipment = (equipmentId, limit = 100) =>
  client.get(`/api/predictions/${equipmentId}`, { params: { limit } }).then((r) => r.data)

export const getDashboardSummary = () => client.get('/api/dashboard/summary').then((r) => r.data)

export const getRecentPredictions = (limit = 10) =>
  client.get('/api/dashboard/recent-predictions', { params: { limit } }).then((r) => r.data)

export const getRiskDistribution = () =>
  client.get('/api/dashboard/risk-distribution').then((r) => r.data)

export const getAIRecommendation = (data) =>
  client.post('/api/ai/recommendation', data).then((r) => r.data)
