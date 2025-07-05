import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Package, Save, ArrowLeft } from 'lucide-react';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import './AddProduct.css'; // נשתמש באותו CSS כמו AddProduct

const EditProduct = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    sku: '',
    category: '',
    price: '',
    quantity: '',
    min_stock_level: ''
  });

  useEffect(() => {
    loadProduct();
  }, [id]);

  const loadProduct = async () => {
    try {
      setLoadingData(true);
      const response = await apiService.getProduct(id);
      const product = response.data;
      
      setFormData({
        name: product.name || '',
        description: product.description || '',
        sku: product.sku || '',
        category: product.category || '',
        price: product.price?.toString() || '',
        quantity: product.quantity?.toString() || '',
        min_stock_level: product.min_stock_level?.toString() || ''
      });
    } catch (error) {
      console.error('Error loading product:', error);
      toast.error('Failed to load product');
      navigate('/products');
    } finally {
      setLoadingData(false);
    }
  };

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
      
      await apiService.updateProduct(id, productData);
      toast.success('Product updated successfully!');
      navigate(`/products/${id}`);
    } catch (error) {
      console.error('Error updating product:', error);
      if (error.response?.data?.message) {
        toast.error(error.response.data.message);
      } else {
        toast.error('Failed to update product');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <div className="add-product">
        <div className="add-product-loading">
          <div className="loading-spinner">
            <Package className="animate-spin" size={32} />
          </div>
          <p>Loading product...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="add-product">
      <div className="add-product-header">
        <button 
          className="back-button"
          onClick={() => navigate(`/products/${id}`)}
        >
          <ArrowLeft size={20} />
          Back to Product
        </button>
        <div>
          <h1 className="add-product-title">Edit Product</h1>
          <p className="add-product-subtitle">Update product information</p>
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
                <label htmlFor="quantity">Current Quantity *</label>
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
                onClick={() => navigate(`/products/${id}`)}
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
                  'Updating...'
                ) : (
                  <>
                    <Save size={16} />
                    Update Product
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

export default EditProduct;