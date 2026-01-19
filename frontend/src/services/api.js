import axios from 'axios'

const API_URL = '/api'

export const api = {
  getStats: async () => {
    const response = await axios.get(`${API_URL}/stats`)
    return response.data
  },

  search: async (params) => {
    const response = await axios.get(`${API_URL}/search`, { params })
    return response.data
  },

  getRecipe: async (id) => {
    const response = await axios.get(`${API_URL}/recipes/${id}`)
    return response.data
  },

  getCategories: async () => {
    const response = await axios.get(`${API_URL}/categories`)
    return response.data
  }
}