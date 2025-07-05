import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Package, 
  AlertTriangle, 
  TrendingUp, 
  ShoppingCart,
  Plus,
  RefreshCw
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import './Dashboard.css';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState(null);
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const [recentRestocks, setRecentRestocks] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load analytics data
      const analyticsResponse = await apiService.getAnalytics();
      setAnalytics(analyticsResponse.data);
      
      // Load low stock products - בדיקה שזה array
      const lowStockResponse = await apiService.getLowStockProducts();
      const lowStockData = Array.isArray(lowStockResponse.data) 
        ? lowStockResponse.data 
        : (lowStockResponse.data.products || []);
      setLowStockProducts(lowStockData.slice(0, 5)); // Show only first 5
      
      // Load recent restocks - בדיקה שזה array
      const restocksResponse = await apiService.getRestockHistory();
      const restocksData = Array.isArray(restocksResponse.data) 
        ? restocksResponse.data 
        : (restocksResponse.data.restocks || []);
      setRecentRestocks(restocksData.slice(0, 5)); // Show only first 5
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
      // ודא שכל המשתנים הם arrays במקרה של שגיאה
      setLowStockProducts([]);
      setRecentRestocks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    loadDashboardData();
    toast.success('Dashboard refreshed');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner">
          <RefreshCw className="animate-spin" size={32} />
        </div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  const stats = [
    {
      title: 'Total Products',
      value: analytics?.total_products || 0,
      icon: Package,
      color: 'blue',
      trend: '+12%'
    },
    {
      title: 'Low Stock Items',
      value: analytics?.low_stock_count || 0,
      icon: AlertTriangle,
      color: 'red',
      trend: '-5%'
    },
    {
      title: 'Total Value',
      value: `$${analytics?.total_value?.toLocaleString() || '0'}`,
      icon: TrendingUp,
      color: 'green',
      trend: '+8%'
    },
    {
      title: 'Recent Restocks',
      value: analytics?.recent_restocks || 0,
      icon: ShoppingCart,
      color: 'purple',
      trend: '+15%'
    }
  ];

  // Mock data for charts - replace with real data from your API
  const chartData = [
    { name: 'Jan', products: 120, value: 25000 },
    { name: 'Feb', products: 135, value: 28000 },
    { name: 'Mar', products: 148, value: 32000 },
    { name: 'Apr', products: 156, value: 35000 },
    { name: 'May', products: 142, value: 31000 },
    { name: 'Jun', products: 168, value: 38000 },
  ];

  const categoryData = [
    { name: 'Electronics', count: 45 },
    { name: 'Clothing', count: 32 },
    { name: 'Books', count: 28 },
    { name: 'Home', count: 23 },
    { name: 'Sports', count: 18 },
  ];

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">Overview of your inventory management</p>
        </div>
        <div className="dashboard-actions">
          <button className="btn btn-secondary" onClick={handleRefresh}>
            <RefreshCw size={16} />
            Refresh
          </button>
          <Link to="/products/add" className="btn btn-primary">
            <Plus size={16} />
            Add Product
          </Link>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className={`stat-card stat-card-${stat.color}`}>
              <div className="stat-card-content">
                <div className="stat-card-main">
                  <div className="stat-card-icon">
                    <Icon size={24} />
                  </div>
                  <div className="stat-card-info">
                    <h3 className="stat-card-value">{stat.value}</h3>
                    <p className="stat-card-title">{stat.title}</p>
                  </div>
                </div>
                <div className="stat-card-trend">
                  <span className={`trend ${stat.trend.startsWith('+') ? 'positive' : 'negative'}`}>
                    {stat.trend}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <div className="chart-header">
            <h2>Inventory Trends</h2>
            <p>Product count and value over time</p>
          </div>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="products" stroke="#667eea" strokeWidth={2} />
                <Line type="monotone" dataKey="value" stroke="#764ba2" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-container">
          <div className="chart-header">
            <h2>Products by Category</h2>
            <p>Distribution of products across categories</p>
          </div>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Quick Actions & Alerts */}
      <div className="dashboard-bottom">
        {/* Low Stock Alert */}
        <div className="alert-section">
          <div className="section-header">
            <h2>Low Stock Alerts</h2>
            <Link to="/products?filter=low-stock" className="section-link">
              View All
            </Link>
          </div>
          {lowStockProducts.length > 0 ? (
            <div className="alert-list">
              {lowStockProducts.map((product) => (
                <div key={product.id} className="alert-item">
                  <div className="alert-icon">
                    <AlertTriangle size={20} />
                  </div>
                  <div className="alert-content">
                    <h4>{product.name}</h4>
                    <p>Only {product.quantity} left in stock</p>
                  </div>
                  <div className="alert-actions">
                    <Link to={`/products/${product.id}`} className="btn btn-sm btn-primary">
                      Restock
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No low stock alerts at the moment</p>
            </div>
          )}
        </div>

        {/* Recent Activity */}
        <div className="activity-section">
          <div className="section-header">
            <h2>Recent Activity</h2>
            <Link to="/analytics" className="section-link">
              View All
            </Link>
          </div>
          {recentRestocks.length > 0 ? (
            <div className="activity-list">
              {recentRestocks.map((restock, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-icon">
                    <ShoppingCart size={16} />
                  </div>
                  <div className="activity-content">
                    <p><strong>{restock.product_name}</strong> restocked</p>
                    <p className="activity-meta">
                      +{restock.quantity} units • {new Date(restock.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No recent activity</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;