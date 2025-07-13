import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiService = {
  // Products
  getProducts: async () => {
    const response = await axios.get(`${API_BASE_URL}/products`);
    return response;
  },

  getProduct: async (id) => {
    const response = await axios.get(`${API_BASE_URL}/products/${id}`);
    return response;
  },

  createProduct: async (productData) => {
    const response = await axios.post(`${API_BASE_URL}/products`, productData);
    return response;
  },

  updateProduct: async (id, productData) => {
    const response = await axios.put(`${API_BASE_URL}/products/${id}`, productData);
    return response;
  },

  deleteProduct: async (id) => {
    const response = await axios.delete(`${API_BASE_URL}/products/${id}`);
    return response;
  },

  // Restock
  restockProduct: async (id, restockData) => {
    const response = await axios.post(`${API_BASE_URL}/products/${id}/restock`, restockData);
    return response;
  },

  getRestockHistory: async (productId) => {
    const url = productId 
      ? `${API_BASE_URL}/restocks?product_id=${productId}`
      : `${API_BASE_URL}/restocks`;
    const response = await axios.get(url);
    return response;
  },

  // Analytics
  getAnalytics: async () => {
    const response = await axios.get(`${API_BASE_URL}/products/analytics`);
    return response;
  },

  // Low stock products
  getLowStockProducts: async () => {
    const response = await axios.get(`${API_BASE_URL}/products/low-stock`);
    return response;
  },

  // Health check
  healthCheck: async () => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response;
  }
};

export { apiService };