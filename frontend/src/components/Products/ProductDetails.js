import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Package, 
  Edit, 
  Trash2, 
  Plus,
  AlertTriangle,
  Calendar,
  DollarSign,
  Hash,
  Tag,
  BarChart3
} from 'lucide-react';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import RestockModal from './RestockModal';
import './ProductDetails.css';

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [restockHistory, setRestockHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showRestockModal, setShowRestockModal] = useState(false);

  useEffect(() => {
    loadProduct();
    loadRestockHistory();
  }, [id]);

  const loadProduct = async () => {
    try {
      setLoading(true);
      const response = await apiService.getProduct(id);
      setProduct(response.data);
    } catch (error) {
      console.error('Error loading product:', error);
      toast.error('Failed to load product details');
      navigate('/products');
    } finally {
      setLoading(false);
    }
  };

  const loadRestockHistory = async () => {
    try {
      const response = await apiService.getRestockHistory();
      // Filter restocks for this specific product
      const productRestocks = response.data.filter(restock => 
        restock.product_id === parseInt(id)
      );
      setRestockHistory(productRestocks);
    } catch (error) {
      console.error('Error loading restock history:', error);
    }
  };

  const handleDeleteProduct = async () => {
    if (!window.confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
      return;
    }

    try {
      await apiService.deleteProduct(id);
      toast.success('Product deleted successfully');
      navigate('/products');
    } catch (error) {
      console.error('Error deleting product:', error);
      toast.error('Failed to delete product');
    }
  };

  const handleRestockSuccess = () => {
    setShowRestockModal(false);
    loadProduct();
    loadRestockHistory();
  };

  const getStockStatus = () => {
    if (!product) return { class: '', label: '' };
    
    if (product.quantity === 0) {
      return { class: 'status-danger', label: 'Out of Stock' };
    } else if (product.quantity <= (product.min_stock_level || 10)) {
      return { class: 'status-warning', label: 'Low Stock' };
    } else {
      return { class: 'status-success', label: 'In Stock' };
    }
  };

  if (loading) {
    return (
      <div className="product-details-loading">
        <div className="loading-spinner">
          <Package className="animate-spin" size={32} />
        </div>
        <p>Loading product details...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="product-not-found">
        <Package size={64} />
        <h2>Product Not Found</h2>
        <p>The product you're looking for doesn't exist or has been deleted.</p>
        <Link to="/products" className="btn btn-primary">
          <ArrowLeft size={16} />
          Back to Products
        </Link>
      </div>
    );
  }

  const stockStatus = getStockStatus();

  return (
    <div className="product-details">
      {/* Header */}
      <div className="product-header">
        <Link to="/products" className="back-button">
          <ArrowLeft size={20} />
          Back to Products
        </Link>
        
        <div className="product-title-section">
          <div className="product-icon-large">
            <Package size={32} />
          </div>
          <div>
            <h1 className="product-title">{product.name}</h1>
            <p className="product-sku">SKU: {product.sku}</p>
          </div>
        </div>

        <div className="product-actions">
          <button 
            className="btn btn-primary"
            onClick={() => setShowRestockModal(true)}
          >
            <Plus size={16} />
            Restock
          </button>
          <Link to={`/products/${id}/edit`} className="btn btn-secondary">
            <Edit size={16} />
            Edit
          </Link>
          <button 
            className="btn btn-danger"
            onClick={handleDeleteProduct}
          >
            <Trash2 size={16} />
            Delete
          </button>
        </div>
      </div>

      {/* Product Info Grid */}
      <div className="product-info-grid">
        {/* Basic Information */}
        <div className="info-card">
          <div className="info-card-header">
            <Package size={20} />
            <h2>Basic Information</h2>
          </div>
          <div className="info-card-content">
            <div className="info-row">
              <span className="info-label">Name:</span>
              <span className="info-value">{product.name}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Description:</span>
              <span className="info-value">{product.description || 'No description'}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Category:</span>
              <span className="info-value">
                <span className="category-badge">
                  <Tag size={14} />
                  {product.category || 'Uncategorized'}
                </span>
              </span>
            </div>
            <div className="info-row">
              <span className="info-label">SKU:</span>
              <span className="info-value">
                <span className="sku-badge">
                  <Hash size={14} />
                  {product.sku}
                </span>
              </span>
            </div>
          </div>
        </div>

        {/* Stock Information */}
        <div className="info-card">
          <div className="info-card-header">
            <BarChart3 size={20} />
            <h2>Stock Information</h2>
          </div>
          <div className="info-card-content">
            <div className="stock-overview">
              <div className="stock-metric">
                <span className="stock-number">{product.quantity}</span>
                <span className="stock-label">Current Stock</span>
              </div>
              <div className="stock-metric">
                <span className="stock-number">{product.min_stock_level || 10}</span>
                <span className="stock-label">Minimum Level</span>
              </div>
              <div className="stock-status-large">
                <span className={`status-badge ${stockStatus.class}`}>
                  {stockStatus.class === 'status-warning' && <AlertTriangle size={16} />}
                  {stockStatus.label}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Pricing Information */}
        <div className="info-card">
          <div className="info-card-header">
            <DollarSign size={20} />
            <h2>Pricing</h2>
          </div>
          <div className="info-card-content">
            <div className="price-display">
              <span className="price-amount">${product.price}</span>
              <span className="price-label">Unit Price</span>
            </div>
            <div className="price-calculations">
              <div className="calc-row">
                <span>Total Value:</span>
                <span className="calc-value">
                  ${(product.price * product.quantity).toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Timestamps */}
        <div className="info-card">
          <div className="info-card-header">
            <Calendar size={20} />
            <h2>Timeline</h2>
          </div>
          <div className="info-card-content">
            <div className="info-row">
              <span className="info-label">Created:</span>
              <span className="info-value">
                {new Date(product.created_at).toLocaleDateString()}
              </span>
            </div>
            <div className="info-row">
              <span className="info-label">Last Updated:</span>
              <span className="info-value">
                {new Date(product.updated_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Restock History */}
      <div className="restock-history-section">
        <div className="section-header">
          <h2>Restock History</h2>
          <span className="history-count">
            {restockHistory.length} {restockHistory.length === 1 ? 'entry' : 'entries'}
          </span>
        </div>
        
        {restockHistory.length > 0 ? (
          <div className="restock-table-container">
            <table className="restock-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Quantity Added</th>
                  <th>Previous Stock</th>
                  <th>New Stock</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {restockHistory.map((restock, index) => (
                  <tr key={index}>
                    <td>{new Date(restock.created_at).toLocaleDateString()}</td>
                    <td>
                      <span className="quantity-added">+{restock.quantity_added}</span>
                    </td>
                    <td>{restock.previous_stock}</td>
                    <td>{restock.new_stock}</td>
                    <td>{restock.reason || 'Manual restock'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-history">
            <BarChart3 size={48} />
            <h3>No Restock History</h3>
            <p>This product hasn't been restocked yet.</p>
            <button 
              className="btn btn-primary"
              onClick={() => setShowRestockModal(true)}
            >
              <Plus size={16} />
              Add First Restock
            </button>
          </div>
        )}
      </div>

      {/* Restock Modal */}
      {showRestockModal && (
        <RestockModal
          product={product}
          onClose={() => setShowRestockModal(false)}
          onSuccess={handleRestockSuccess}
        />
      )}
    </div>
  );
};

export default ProductDetails;