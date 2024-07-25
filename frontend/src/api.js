import axios from 'axios'

// Create an Axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/', // Adjust this URL to backend server
})

// Add a request interceptor to include the JWT token in headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Optionally add a response interceptor to handle token expiration and refreshing tokens
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/users/refresh/', {
            refresh: refreshToken,
          })
          localStorage.setItem('access_token', response.data.access)
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access
          return api(originalRequest)
        } catch (error) {
          console.error('Token refresh error', error)
        }
      }
    }
    return Promise.reject(error)
  },
)

export default api
