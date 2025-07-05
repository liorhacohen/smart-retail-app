import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, Save, ArrowLeft } from 'lucide-react';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import './AddProduct.css';

const AddProduct = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    sku: '',
    category: '',
    price: '',
    quantity: '',
    min_stock_level: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.name.trim()) {
      toast.error('Product name is required');
      return;
    }
    
    if (!formData.sku.trim()) {
      toast.error('SKU is required');
      return;
    }
    
    if (!formData.price || parseFloat(formData.price) <= 0) {
      toast.error('Valid price is required');
      return;
    }
    
    if (!formData.quantity || parseInt(formData.quantity) < 0) {
      toast.error('Valid quantity is required');
      return;
    }

    try {
      setLoading(true);
      
      const productData = {
        ...formData,
        price: parseFloat(formData.price),
        quantity: parseInt(formData.quantity),
        min_stock_level: parseInt(formData.min_stock_level) || 10
      };
      
      await apiService.createProduct(productData);
      toast.success('Product created successfully!');
      navigate('/products');
    } catch (error) {
      console.error('Error creating product:', error);
      if (error.response?.data?.message) {
        toast.error(error.response.data.message);
      } else {
        toast.error('Failed to create product');
      }
    } finally {
      setLoading(false);
    }
  };

  const generateSKU = () => {
    const timestamp = Date.now().toString().slice(-6);
    const randomStr = Math.random().toString(36).substring(2, 5).toUpperCase();
    return `SKU-${randomStr}-${timestamp}`;
  };

  const handleGenerateSKU = () => {
    setFormData(prev => ({
      ...prev,
      sku: generateSKU()
    }));
  };

  return (
    <div className="add-product">
      <div className="add-product-header">
        <button 
          className="back-button"
          onClick={() => navigate('/products')}
        >
          <ArrowLeft size={20} />
          Back to Products
        </button>
        <div>
          <h1 className="add-product-title">Add New Product</h1>
          <p className="add-product-subtitle">Create a new product for your inventory</p>
        </div>
      </div>

      <div className="add-product-container">
        <div className="add-product-card">
          <div className="card-header">
            <Package className="card-icon" />
            <h2>Product Information</h2>
          </div>

          <form onSubmit={handleSubmit} className="product-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="name">Product Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter product name"
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="category">Category</label>
                <input
                  type="text"
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  placeholder="e.g., Electronics, Clothing"
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Enter product description"
                rows="3"
                className="form-textarea"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="sku">SKU *</label>
                <div className="sku-input-group">
                  <input
                    type="text"
                    id="sku"
                    name="sku"
                    value={formData.sku}
                    onChange={handleChange}
                    placeholder="Enter SKU"
                    required
                    className="form-input"
                  />
                  <button
                    type="button"
                    onClick={handleGenerateSKU}
                    className="generate-sku-btn"
                  >
                    Generate
                  </button>
                </div>
                <small className="form-help">Unique product identifier</small>
              </div>

              <div className="form-group">
                <label htmlFor="price">Price ($) *</label>
                <input
                  type="number"
                  id="price"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                  placeholder="0.00"
                  min="0"
                  step="0.01"
                  required
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="quantity">Initial Quantity *</label>
                <input
                  type="number"
                  id="quantity"
                  name="quantity"
                  value={formData.quantity}
                  onChange={handleChange}
                  placeholder="0"
                  min="0"
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="min_stock_level">Minimum Stock Level</label>
                <input
                  type="number"
                  id="min_stock_level"
                  name="min_stock_level"
                  value={formData.min_stock_level}
                  onChange={handleChange}
                  placeholder="10"
                  min="0"
                  className="form-input"
                />
                <small className="form-help">Alert when stock falls below this level</small>
              </div>
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={() => navigate('/products')}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  'Creating...'
                ) : (
                  <>
                    <Save size={16} />
                    Create Product
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddProduct;