import axios from 'axios'

const API_BASE = '/api'

// Configure axios instance
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.message)
    return Promise.reject(error)
  }
)

export const searchAPI = {
  // Search records by query
  search: async (query, limit = 50, offset = 0) => {
    const response = await apiClient.get('/search', {
      params: { q: query, limit, offset }
    })
    return response.data
  },

  // Get autocomplete suggestions
  autocomplete: async (query, limit = 10) => {
    const response = await apiClient.get('/search/autocomplete', {
      params: { q: query, limit }
    })
    return response.data
  },

  // Get record by ID
  getRecord: async (recordId) => {
    const response = await apiClient.get(`/records/${recordId}`)
    return response.data
  },

  // Get all stores
  getStores: async () => {
    const response = await apiClient.get('/stores')
    return response.data
  },

  // Get specific store
  getStore: async (storeId) => {
    const response = await apiClient.get(`/stores/${storeId}`)
    return response.data
  },

  // Trigger manual scrape (admin)
  triggerScrape: async () => {
    const response = await apiClient.post('/stores/trigger-scrape')
    return response.data
  },
}

export default apiClient
