import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Suppress backend connection errors (app uses mock data)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Silently handle backend connection errors
    if (error.code === 'ERR_NETWORK' || error.message.includes('ERR_FAILED')) {
      return Promise.reject({ silent: true, ...error });
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
};

// Restaurant APIs
export const restaurantAPI = {
  getAll: (params) => api.get('/restaurants', { params }),
  getById: (id) => api.get(`/restaurants/${id}`),
  getMenu: (id) => api.get(`/restaurants/${id}/menu`),
};

// Order APIs
export const orderAPI = {
  create: (data) => api.post('/orders', data),
  getHistory: () => api.get('/orders/history'),
};

// AI Assistant API
export const aiAPI = {
  chat: (data) => api.post('/ai/order-assistant', data),
};

export default api;
