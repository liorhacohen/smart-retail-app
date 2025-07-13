import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Package, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import './Analytics.css';

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [restockHistory, setRestockHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const [analyticsResponse, restocksResponse] = await Promise.all([
          apiService.getAnalytics(),
          apiService.getRestockHistory()
        ]);
        
        setAnalytics(analyticsResponse.data.analytics);
        setRestockHistory(restocksResponse.data.restock_logs || []);
      } catch (error) {
        toast.error('Failed to load analytics data');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="analytics-loading">
        <div className="loading-spinner">
          <BarChart3 className="animate-spin" size={32} />
        </div>
        <p>Loading analytics...</p>
      </div>
    );
  }

  // Mock data for demonstration - replace with real data from your API
  const categoryData = [
    { name: 'Electronics', value: 45, color: '#667eea' },
    { name: 'Clothing', value: 32, color: '#764ba2' },
    { name: 'Books', value: 28, color: '#f093fb' },
    { name: 'Home', value: 23, color: '#4facfe' },
    { name: 'Sports', value: 18, color: '#43e97b' },
  ];

  const monthlyData = [
    { month: 'Jan', restocks: 12, products_added: 8 },
    { month: 'Feb', restocks: 19, products_added: 12 },
    { month: 'Mar', restocks: 15, products_added: 6 },
    { month: 'Apr', restocks: 22, products_added: 15 },
    { month: 'May', restocks: 18, products_added: 9 },
    { month: 'Jun', restocks: 25, products_added: 18 },
  ];

  const topProducts = [
    { name: 'iPhone 14', restocks: 15, total_quantity: 450 },
    { name: 'Samsung TV', restocks: 12, total_quantity: 320 },
    { name: 'Nike Shoes', restocks: 10, total_quantity: 280 },
    { name: 'Laptop Dell', restocks: 8, total_quantity: 190 },
    { name: 'Coffee Maker', restocks: 6, total_quantity: 150 },
  ];

  return (
    <div className="analytics">
      <div className="analytics-header">
        <div>
          <h1 className="analytics-title">Analytics & Reports</h1>
          <p className="analytics-subtitle">Insights into your inventory performance</p>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon metric-blue">
            <Package size={24} />
          </div>
          <div className="metric-content">
            <h3>{analytics?.total_products || 146}</h3>
            <p>Total Products</p>
            <span className="metric-change positive">+12% from last month</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon metric-green">
            <TrendingUp size={24} />
          </div>
          <div className="metric-content">
            <h3>${analytics?.total_value?.toLocaleString() || '284,760'}</h3>
            <p>Total Inventory Value</p>
            <span className="metric-change positive">+8% from last month</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon metric-red">
            <AlertTriangle size={24} />
          </div>
          <div className="metric-content">
            <h3>{analytics?.low_stock_count || 23}</h3>
            <p>Low Stock Items</p>
            <span className="metric-change negative">-15% from last month</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon metric-purple">
            <BarChart3 size={24} />
          </div>
          <div className="metric-content">
            <h3>{restockHistory?.length || 89}</h3>
            <p>Total Restocks</p>
            <span className="metric-change positive">+25% from last month</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Monthly Activity */}
        <div className="chart-card full-width">
          <div className="chart-header">
            <h2>Monthly Activity</h2>
            <p>Restocks and new products over time</p>
          </div>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="restocks" fill="#667eea" name="Restocks" />
                <Bar dataKey="products_added" fill="#764ba2" name="New Products" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Distribution */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Product Categories</h2>
            <p>Distribution by category</p>
          </div>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Products */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Most Restocked Products</h2>
            <p>Products requiring frequent restocking</p>
          </div>
          <div className="top-products-list">
            {topProducts.map((product, index) => (
              <div key={index} className="top-product-item">
                <div className="product-rank">{index + 1}</div>
                <div className="product-details">
                  <h4>{product.name}</h4>
                  <p>{product.restocks} restocks • {product.total_quantity} units</p>
                </div>
                <div className="product-bar">
                  <div 
                    className="product-bar-fill" 
                    style={{ width: `${(product.restocks / 15) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity Table */}
      <div className="activity-card">
        <div className="activity-header">
          <h2>Recent Restock Activity</h2>
          <p>Latest inventory movements</p>
        </div>
        <div className="activity-table-container">
          <table className="activity-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Quantity Added</th>
                <th>Reason</th>
                <th>Date</th>
                <th>User</th>
              </tr>
            </thead>
            <tbody>
            {(restockHistory || []).slice(0, 10).map((restock, index) => (
                <tr key={index}>
                  <td>
                    <div className="product-name">{restock.product_name}</div>
                  </td>
                  <td>
                    <span className="quantity-badge">+{restock.quantity}</span>
                  </td>
                  <td>{restock.reason || 'Manual restock'}</td>
                  <td>{new Date(restock.created_at).toLocaleDateString()}</td>
                  <td>Store Manager</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Analytics;