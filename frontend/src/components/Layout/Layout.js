import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Package, 
  PlusCircle, 
  BarChart3, 
  Menu, 
  X,
  Store
} from 'lucide-react';
import './Layout.css';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Products', href: '/products', icon: Package },
    { name: 'Add Product', href: '/products/add', icon: PlusCircle },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  ];

  const isActiveRoute = (href) => {
    return location.pathname === href;
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      setSidebarOpen(false);
    }
  };

  const handleOverlayKeyDown = (e) => {
    if (e.key === 'Escape') {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="layout">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="sidebar-overlay"
          onClick={handleOverlayClick}
          onKeyDown={handleOverlayKeyDown}
          role="button"
          tabIndex={0}
          aria-label="Close sidebar"
        />
      )}

      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <Store className="sidebar-logo-icon" />
            <span className="sidebar-logo-text">InventoryPro</span>
          </div>
          <button 
            className="sidebar-close-btn"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <nav className="sidebar-nav">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`sidebar-nav-item ${isActiveRoute(item.href) ? 'active' : ''}`}
                onClick={() => setSidebarOpen(false)}
              >
                <Icon className="sidebar-nav-icon" size={20} />
                <span className="sidebar-nav-text">{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Main content */}
      <div className="main-content">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <button
              className="mobile-menu-btn"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu size={24} />
            </button>
            
            <h1 className="header-title">
              {navigation.find(item => isActiveRoute(item.href))?.name || 'Inventory Management'}
            </h1>
            
            <div className="header-actions">
              <span className="user-info">Store Manager</span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;