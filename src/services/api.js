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

// Address APIs
export const addressAPI = {
  getAll: () => api.get('/addresses'),
  create: (data) => api.post('/addresses', data),
  update: (id, data) => api.put(`/addresses/${id}`, data),
  delete: (id) => api.delete(`/addresses/${id}`),
  setDefault: (id) => api.put(`/addresses/${id}/set-default`),
  setCurrent: (id) => api.put('/addresses/current', { address_id: id }),
};

// Cart APIs
export const cartAPI = {
  getCart: () => api.get('/cart'),
  addItem: (data) => api.post('/cart/add', data),
  updateItem: (itemId, data) => api.put(`/cart/update/${itemId}`, data),
  removeItem: (itemId) => api.delete(`/cart/remove/${itemId}`),
  clearCart: () => api.delete('/cart/clear'),
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
