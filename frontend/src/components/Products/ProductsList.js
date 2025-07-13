import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Package, 
  Plus, 
  Search, 
  Eye,
  Edit,
  Trash2,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import './ProductsList.css';

const ProductsList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await apiService.getProducts();
      setProducts(response.data.products);
    } catch (error) {
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await apiService.getProducts();
        setProducts(response.data.products);
      } catch (error) {
        toast.error('Failed to load products');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const filterProducts = () => {
    return products.filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           product.category.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = !filterCategory || product.category === filterCategory;
      return matchesSearch && matchesCategory;
    });
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await apiService.deleteProduct(productId);
      setProducts(products.filter(p => p.id !== productId));
      toast.success('Product deleted successfully');
    } catch (error) {
      toast.error('Failed to delete product');
    }
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
          <button className="btn btn-secondary" onClick={fetchProducts}>
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
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="filter-select"
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Products Table */}
      <div className="products-table-container">
        {filterProducts().length > 0 ? (
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
              {filterProducts().map((product) => {
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
                          onClick={() => { /* handleRestock(product) */ }} // handleRestock removed
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
              {searchTerm || filterCategory
                ? 'Try adjusting your filters'
                : 'Get started by adding your first product'
              }
            </p>
            {!searchTerm && !filterCategory && (
              <Link to="/products/add" className="btn btn-primary">
                <Plus size={16} />
                Add Your First Product
              </Link>
            )}
          </div>
        )}
      </div>

      {/* Restock Modal */}
      {/* showRestockModal && selectedProduct && ( */}
      {/*   <RestockModal */}
      {/*     product={selectedProduct} */}
      {/*     onClose={() => setShowRestockModal(false)} */}
      {/*     onSuccess={handleRestockSuccess} */}
      {/*   /> */}
      {/* ) */}
    </div>
  );
};

export default ProductsList;