import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import { 
  Search, 
  Filter, 
  Plus, 
  Edit, 
  Trash2, 
  Package, 
  AlertTriangle,
  RefreshCw,
  Eye
} from 'lucide-react';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import RestockModal from './RestockModal';
import './ProductsList.css';

const ProductsList = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [stockFilter, setStockFilter] = useState('');
  const [showRestockModal, setShowRestockModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    loadProducts();
  }, []);

  useEffect(() => {
    filterProducts();
  }, [products, searchTerm, selectedCategory, stockFilter]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const response = await apiService.getProducts();
      
      // בדיקה שהתגובה היא array
      const productsData = Array.isArray(response.data) ? response.data : [];
      setProducts(productsData);
      
      console.log('Products loaded:', productsData); // לבדיקה
    } catch (error) {
      console.error('Error loading products:', error);
      toast.error('Failed to load products');
      setProducts([]); // ודא שזה array גם במקרה של שגיאה
    } finally {
      setLoading(false);
    }
  };

  const filterProducts = () => {
    let filtered = [...products];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.sku.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Category filter
    if (selectedCategory) {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    // Stock filter
    if (stockFilter === 'low') {
      filtered = filtered.filter(product => product.quantity <= product.min_stock_level);
    } else if (stockFilter === 'out') {
      filtered = filtered.filter(product => product.quantity === 0);
    } else if (stockFilter === 'in') {
      filtered = filtered.filter(product => product.quantity > product.min_stock_level);
    }

    setFilteredProducts(filtered);
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await apiService.deleteProduct(productId);
      toast.success('Product deleted successfully');
      loadProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
      toast.error('Failed to delete product');
    }
  };

  const handleRestock = (product) => {
    setSelectedProduct(product);
    setShowRestockModal(true);
  };

  const handleRestockSuccess = () => {
    setShowRestockModal(false);
    setSelectedProduct(null);
    loadProducts();
  };

  const getStockStatus = (product) => {
    if (product.quantity === 0) {
      return { status: 'out', label: 'Out of Stock', class: 'stock-out' };
    } else if (product.quantity <= product.min_stock_level) {
      return { status: 'low', label: 'Low Stock', class: 'stock-low' };
    } else {
      return { status: 'in', label: 'In Stock', class: 'stock-in' };
    }
  };

  const categories = [...new Set(products.map(p => p.category))].filter(Boolean);

  if (loading) {
    return (
      <div className="products-loading">
        <div className="loading-spinner">
          <RefreshCw className="animate-spin" size={32} />
        </div>
        <p>Loading products...</p>
      </div>
    );
  }

  return (
    <div className="products-list">
      {/* Header */}
      <div className="products-header">
        <div>
          <h1 className="products-title">Products</h1>
          <p className="products-subtitle">Manage your inventory</p>
        </div>
        <div className="products-actions">
          <button className="btn btn-secondary" onClick={loadProducts}>
            <RefreshCw size={16} />
            Refresh
          </button>
          <Link to="/products/add" className="btn btn-primary">
            <Plus size={16} />
            Add Product
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="products-filters">
        <div className="filter-group">
          <div className="search-box">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
        </div>

        <div className="filter-group">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="filter-select"
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <select
            value={stockFilter}
            onChange={(e) => setStockFilter(e.target.value)}
            className="filter-select"
          >
            <option value="">All Stock Levels</option>
            <option value="in">In Stock</option>
            <option value="low">Low Stock</option>
            <option value="out">Out of Stock</option>
          </select>
        </div>
      </div>

      {/* Products Table */}
      <div className="products-table-container">
        {filteredProducts.length > 0 ? (
          <table className="products-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>SKU</th>
                <th>Category</th>
                <th>Stock</th>
                <th>Price</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredProducts.map((product) => {
                const stockStatus = getStockStatus(product);
                return (
                  <tr key={product.id}>
                    <td>
                      <div className="product-info">
                        <div className="product-icon">
                          <Package size={20} />
                        </div>
                        <div>
                          <div className="product-name">{product.name}</div>
                          <div className="product-description">{product.description}</div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="product-sku">{product.sku}</span>
                    </td>
                    <td>
                      <span className="product-category">{product.category || 'Uncategorized'}</span>
                    </td>
                    <td>
                      <div className="stock-info">
                        <span className="stock-quantity">{product.quantity}</span>
                        <span className="stock-min">Min: {product.min_stock_level}</span>
                      </div>
                    </td>
                    <td>
                      <span className="product-price">${product.price}</span>
                    </td>
                    <td>
                      <span className={`stock-status ${stockStatus.class}`}>
                        {stockStatus.status === 'low' || stockStatus.status === 'out' && (
                          <AlertTriangle size={14} />
                        )}
                        {stockStatus.label}
                      </span>
                    </td>
                    <td>
                      <div className="product-actions">
                        <button
                          className="btn-icon btn-icon-blue"
                          onClick={() => handleRestock(product)}
                          title="Restock"
                        >
                          <Plus size={16} />
                        </button>
                        <Link
                          to={`/products/${product.id}`}
                          className="btn-icon btn-icon-gray"
                          title="View Details"
                        >
                          <Eye size={16} />
                        </Link>
                        <Link
                            to={`/products/${product.id}/edit`}
                            className="btn-icon btn-icon-gray"
                            title="Edit Product"
                            >
                            <Edit size={16} />
                        </Link>
                        <button
                          className="btn-icon btn-icon-red"
                          onClick={() => handleDeleteProduct(product.id)}
                          title="Delete Product"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <Package size={48} />
            <h3>No products found</h3>
            <p>
              {searchTerm || selectedCategory || stockFilter
                ? 'Try adjusting your filters'
                : 'Get started by adding your first product'
              }
            </p>
            {!searchTerm && !selectedCategory && !stockFilter && (
              <Link to="/products/add" className="btn btn-primary">
                <Plus size={16} />
                Add Your First Product
              </Link>
            )}
          </div>
        )}
      </div>

      {/* Restock Modal */}
      {showRestockModal && selectedProduct && (
        <RestockModal
          product={selectedProduct}
          onClose={() => setShowRestockModal(false)}
          onSuccess={handleRestockSuccess}
        />
      )}
    </div>
  );
};

export default ProductsList;