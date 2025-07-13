# Smart Retail App - System Architecture

## 🏗️ Overview

The Smart Retail App is a full-stack inventory management system built with modern technologies, designed for scalability, maintainability, and production readiness.

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Technology Stack](#technology-stack)
4. [Component Architecture](#component-architecture)
5. [Data Architecture](#data-architecture)
6. [API Design](#api-design)
7. [Security Architecture](#security-architecture)
8. [Monitoring & Observability](#monitoring--observability)
9. [Deployment Architecture](#deployment-architecture)
10. [Scalability Considerations](#scalability-considerations)

## 🎯 System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React)       │◄──►│   (Flask)       │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │    │   CI/CD         │    │   Kubernetes    │
│   (Prometheus)  │    │   (GitHub)      │    │   (K8s)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🏛️ Architecture Patterns

### 1. **Layered Architecture**
- **Presentation Layer**: React frontend with component-based UI
- **Application Layer**: Flask REST API with business logic
- **Data Layer**: PostgreSQL with SQLAlchemy ORM
- **Infrastructure Layer**: Docker, Kubernetes, monitoring

### 2. **Microservices-Ready Design**
- Stateless API services
- Database-per-service pattern
- Independent deployment capabilities
- Service discovery ready

### 3. **Event-Driven Architecture**
- RESTful API endpoints
- Asynchronous processing capabilities
- Event logging and monitoring

## 🛠️ Technology Stack

### Frontend
```
React 18.2.0
├── React Router DOM (v6.15.0) - Client-side routing
├── Axios (v1.5.0) - HTTP client
├── Lucide React (v0.263.1) - Icon library
├── React Hot Toast (v2.4.1) - Notifications
├── Recharts (v2.8.0) - Data visualization
└── CSS Modules - Styling
```

### Backend
```
Flask 3.0+
├── Flask-CORS - Cross-origin resource sharing
├── Flask-SQLAlchemy - Database ORM
├── Flask-Limiter - Rate limiting
├── Prometheus Client - Metrics collection
├── Python-dotenv - Environment management
└── PostgreSQL - Primary database
```

### Infrastructure
```
Docker & Docker Compose
├── Multi-stage builds
├── Health checks
├── Volume management
└── Network isolation

Kubernetes
├── Deployments
├── Services
├── Ingress controllers
├── ConfigMaps & Secrets
└── Monitoring stack

Monitoring
├── Prometheus - Metrics collection
├── Grafana - Visualization
└── Custom dashboards
```

## 🧩 Component Architecture

### Frontend Components

```
src/
├── components/
│   ├── Layout/
│   │   └── Layout.js - Main application layout
│   ├── Dashboard/
│   │   └── Dashboard.js - Analytics dashboard
│   ├── Products/
│   │   ├── ProductsList.js - Product listing
│   │   ├── ProductDetails.js - Product details
│   │   ├── AddProduct.js - Product creation
│   │   ├── EditProduct.js - Product editing
│   │   └── RestockModal.js - Restock functionality
│   └── Analytics/
│       └── Analytics.js - Analytics views
├── services/
│   └── api.js - API service layer
├── utils/
│   ├── constants.js - Application constants
│   └── helpers.js - Utility functions
└── styles/
    ├── globals.css - Global styles
    └── variables.css - CSS variables
```

### Backend Components

```
backend/
├── app.py - Main Flask application
├── models/
│   ├── Product - Product entity
│   └── RestockLog - Restock history
├── routes/
│   ├── products.py - Product endpoints
│   ├── analytics.py - Analytics endpoints
│   └── health.py - Health checks
├── services/
│   ├── product_service.py - Business logic
│   └── analytics_service.py - Analytics logic
└── utils/
    ├── validators.py - Input validation
    └── metrics.py - Prometheus metrics
```

## 🗄️ Data Architecture

### Database Schema

```sql
-- Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    stock_level INTEGER DEFAULT 0,
    min_stock_threshold INTEGER DEFAULT 10,
    price DECIMAL(10,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restock Logs Table
CREATE TABLE restock_logs (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity_added INTEGER NOT NULL,
    previous_stock INTEGER NOT NULL,
    new_stock INTEGER NOT NULL,
    restocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

### Data Flow

```
1. User Action (Frontend)
   ↓
2. API Request (Axios)
   ↓
3. Flask Route Handler
   ↓
4. Business Logic Service
   ↓
5. Database Operation (SQLAlchemy)
   ↓
6. Response (JSON)
   ↓
7. UI Update (React State)
```

## 🔌 API Design

### RESTful Endpoints

```
Products API
├── GET    /api/products           - List all products
├── GET    /api/products/{id}      - Get product details
├── POST   /api/products           - Create new product
├── PUT    /api/products/{id}      - Update product
├── DELETE /api/products/{id}      - Delete product
└── POST   /api/products/{id}/restock - Restock product

Analytics API
├── GET    /api/products/analytics     - Get analytics
├── GET    /api/products/low-stock     - Get low stock products
└── GET    /api/restocks               - Get restock history

System API
├── GET    /api/health                - Health check
└── GET    /metrics                   - Prometheus metrics
```

### API Response Format

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation successful",
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 100,
    "pages": 2
  }
}
```

## 🔒 Security Architecture

### Security Layers

1. **Input Validation**
   - Request parameter validation
   - SQL injection prevention
   - XSS protection

2. **Rate Limiting**
   - API rate limiting (Flask-Limiter)
   - Per-endpoint limits
   - IP-based throttling

3. **CORS Configuration**
   - Cross-origin resource sharing
   - Allowed origins configuration
   - Method restrictions

4. **Security Headers**
   - X-Content-Type-Options
   - X-Frame-Options
   - X-XSS-Protection
   - Strict-Transport-Security

5. **Environment Security**
   - Environment variable management
   - Secrets management (Kubernetes)
   - Database connection security

## 📊 Monitoring & Observability

### Metrics Collection

```
Prometheus Metrics
├── HTTP Request Metrics
│   ├── Request count by endpoint
│   ├── Request latency
│   └── Error rates
├── Business Metrics
│   ├── Product stock levels
│   ├── Low stock alerts
│   ├── Restock operations
│   └── Product operations
└── System Metrics
    ├── Database connections
    ├── Memory usage
    └── CPU utilization
```

### Logging Strategy

```
Log Levels
├── ERROR - Application errors
├── WARN  - Warning conditions
├── INFO  - General information
└── DEBUG - Detailed debugging

Log Categories
├── API Requests
├── Database Operations
├── Business Logic
└── System Events
```

### Health Checks

```
Health Endpoints
├── /api/health - Application health
├── /metrics - Prometheus metrics
└── Database connectivity checks
```

## 🚀 Deployment Architecture

### Local Development

```
Docker Compose
├── Frontend (React Dev Server)
├── Backend (Flask Development)
├── Database (PostgreSQL)
└── Monitoring (Prometheus + Grafana)
```

### Production Deployment

```
Kubernetes Cluster
├── Ingress Controller
├── Application Pods
│   ├── Frontend Deployment
│   ├── Backend Deployment
│   └── Database StatefulSet
├── Services
│   ├── Frontend Service
│   ├── Backend Service
│   └── Database Service
├── Monitoring Stack
│   ├── Prometheus
│   └── Grafana
└── ConfigMaps & Secrets
```

### CI/CD Pipeline

```
GitHub Actions
├── Code Quality
│   ├── Linting
│   ├── Testing
│   └── Security scanning
├── Build Process
│   ├── Docker image building
│   ├── Image scanning
│   └── Image pushing
├── Deployment
│   ├── Kubernetes deployment
│   ├── Health checks
│   └── Rollback capability
└── Monitoring
    ├── Deployment verification
    ├── Performance testing
    └── Alert notifications
```

## 📈 Scalability Considerations

### Horizontal Scaling

1. **Stateless Design**
   - No session storage in application
   - Database as single source of truth
   - Load balancer ready

2. **Database Scaling**
   - Connection pooling
   - Read replicas (future)
   - Database sharding (future)

3. **Caching Strategy**
   - Redis integration (future)
   - API response caching
   - Static asset caching

### Performance Optimization

1. **Frontend**
   - Code splitting
   - Lazy loading
   - Bundle optimization

2. **Backend**
   - Database query optimization
   - Connection pooling
   - Async processing

3. **Infrastructure**
   - CDN integration
   - Load balancing
   - Auto-scaling

## 🔄 Data Flow Diagrams

### Product Management Flow

```
User → Frontend → API → Database
  ↓
Product Created/Updated
  ↓
Analytics Updated
  ↓
Metrics Recorded
  ↓
UI Refreshed
```

### Restock Flow

```
User → Restock Modal → API → Database
  ↓
Stock Level Updated
  ↓
Restock Log Created
  ↓
Low Stock Alert Check
  ↓
Metrics Updated
  ↓
UI Updated
```

## 🎯 Future Enhancements

### Planned Features

1. **Advanced Analytics**
   - Predictive analytics
   - Trend analysis
   - Forecasting

2. **Multi-tenancy**
   - User management
   - Role-based access
   - Tenant isolation

3. **Integration Capabilities**
   - Third-party APIs
   - Webhook support
   - Export/Import functionality

4. **Mobile Application**
   - React Native app
   - Offline capabilities
   - Push notifications

## 📚 Documentation

### Related Documents

- [README.md](../README.md) - Project overview
- [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) - Complete setup guide
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures
- [deployment-checklist.md](deployment-checklist.md) - Deployment checklist

---

*This architecture document provides a comprehensive overview of the Smart Retail App's system design, components, and technical decisions. It serves as a reference for developers, DevOps engineers, and stakeholders involved in the project.* 