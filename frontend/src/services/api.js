import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.code === 'ECONNABORTED') {
      error.message = 'Request timeout - please try again';
    } else if (!error.response) {
      error.message = 'Network error - please check your connection';
    } else {
      const status = error.response.status;
      switch (status) {
        case 400:
          error.message = 'Invalid request data';
          break;
        case 404:
          error.message = 'Resource not found';
          break;
        case 500:
          error.message = 'Server error - please try again later';
          break;
        default:
          error.message = error.response.data?.message || 'An error occurred';
      }
    }
    
    return Promise.reject(error);
  }
);

// API Methods
export const apiService = {
  // Health check
  checkHealth: () => api.get('/api/health'),

  // Products
  getProducts: async () => {
    const response = await api.get('/api/products');
    return { data: response.data.products }; 
  },
  getProduct: async (id) => {
    const response = await api.get(`/api/products/${id}`);
    return { data: response.data.product || response.data };
  },
  createProduct: (productData) => api.post('/api/products', productData),
  updateProduct: (id, productData) => api.put(`/api/products/${id}`, productData),
  deleteProduct: (id) => api.delete(`/api/products/${id}`),
  
  // Low stock products
  getLowStockProducts: () => api.get('/api/products/low-stock'),
  
  // Analytics
  getAnalytics: async () => {
    const response = await api.get('/api/products/analytics');
    // התאמת המבנה למה שהDashboard מצפה
    const analytics = response.data.analytics;
    return { 
      data: {
        total_products: analytics.total_products,
        total_value: analytics.total_stock_value,
        low_stock_count: analytics.low_stock_count,
        recent_restocks: analytics.recent_restocks_30_days
      }
    };
  },
  
  // Restock operations
  getRestockHistory: () => api.get('/api/restocks'),
  restockProduct: (id, restockData) => api.post(`/api/products/${id}/restock`, restockData),
};

export default api;