# 🚀 Smart Retail App - Complete Project Guide

## 📋 Project Overview

### **What is this?**
A comprehensive **inventory management system** for retail stores with:
- ✅ **Flask API Backend** - RESTful API for inventory operations
- ✅ **React Frontend** - Modern UI for store managers
- ✅ **PostgreSQL Database** - Reliable data persistence
- ✅ **Docker & Kubernetes** - Production-ready deployment
- ✅ **Prometheus & Grafana** - Real-time monitoring & analytics
- ✅ **Security Features** - Input validation, rate limiting, security headers

### **Key Features**
- **Real-time Stock Tracking** - Monitor inventory levels across all products
- **Low Stock Alerts** - Automatic notifications when items fall below threshold
- **Restocking Management** - Easy restocking operations with full audit trail
- **Analytics Dashboard** - Stock trends and business metrics
- **High Availability** - Multiple replicas and health checks
- **Production Monitoring** - API performance and business metrics

### **Technology Stack**
- **Backend**: Flask (Python) with SQLAlchemy
- **Frontend**: React with modern UI components
- **Database**: PostgreSQL with connection pooling
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (Minikube/EKS)
- **Monitoring**: Prometheus + Grafana
- **Security**: Input validation, rate limiting, security headers

---

## 🚀 Quick Start Commands

### **Start the Application**
```bash
# 1. Start port forwarding for backend and monitoring
kubectl port-forward service/flask-service 5000:5000 &
kubectl port-forward service/grafana-service 3001:3000 &
kubectl port-forward service/prometheus-service 9090:9090 &

# 2. Start the React frontend (in a new terminal)
cd frontend
npm start
```

### **Access URLs**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Prometheus**: http://localhost:9090

### **Stop Port Forwarding**
```bash
# Kill all port forwarding processes
pkill -f "kubectl port-forward"
```

---

## 📚 API Reference

### **Core Endpoints**

| Method | Endpoint | Description | Payload Example |
|--------|----------|-------------|-----------------|
| `GET` | `/api/health` | Health check | None |
| `GET` | `/api/products` | Get all products | None |
| `GET` | `/api/products/<id>` | Get specific product | None |
| `POST` | `/api/products` | Create new product | See below |
| `PUT` | `/api/products/<id>` | Update product | See below |
| `DELETE` | `/api/products/<id>` | Delete product | None |
| `POST` | `/api/products/<id>/restock` | Restock product | See below |
| `GET` | `/api/restocks` | Get restock history | None |
| `GET` | `/api/products/low-stock` | Get low stock products | None |
| `GET` | `/api/products/analytics` | Get analytics | None |
| `GET` | `/metrics` | Prometheus metrics | None |

### **JSON Payload Examples**

#### Create Product
```json
{
  "name": "Wireless Bluetooth Headphones",
  "sku": "WBH-001",
  "description": "Premium wireless headphones with noise cancellation",
  "stock_level": 50,
  "min_stock_threshold": 15,
  "price": 99.99
}
```

#### Update Product
```json
{
  "stock_level": 75,
  "price": 129.99
}
```

#### Restock Product
```json
{
  "quantity": 25,
  "notes": "Weekly inventory replenishment"
}
```

### **Response Format**
All API responses follow this format:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}
```

### **Validation Rules**
- **SKU**: 3-20 alphanumeric characters, hyphens, or underscores
- **Price**: Must be positive number
- **Stock Level**: Must be non-negative integer
- **Quantity**: Must be positive integer for restocking
- **Name**: Required, max 255 characters
- **Description**: Optional, max 1000 characters

---

## 🔧 Deployment Options

### **Option 1: Quick Start (Docker Compose)**
```bash
# Clone and start
git clone <repository-url>
cd smart-retail-app
docker-compose up --build

# Access at http://localhost:5000
```

### **Option 2: Production (Kubernetes)**
```bash
# Build and push image
docker build -t your-username/smart-retail-app:latest .
docker push your-username/smart-retail-app:latest

# Deploy to Kubernetes
kubectl apply -f k8s/configs/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/services/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/ingress/

# Start port forwarding
kubectl port-forward service/flask-service 5000:5000 &
```

### **Option 3: Automated Deployment**
```bash
# Use the automated deployment script
./deploy_with_health_check.sh
```

### **Option 4: Development Setup**
```bash
# Start Minikube
minikube start
minikube addons enable ingress

# Deploy monitoring stack
kubectl apply -f k8s/monitoring/

# Deploy application
kubectl apply -f k8s/
```

---

## 📦 Sample Data Management

### **Overview**
The application includes a comprehensive `sample_products.json` file with 20 realistic products for testing and demonstration purposes. This includes various categories like Electronics, Furniture, Kitchen, Gaming, and Office supplies.

### **Sample Data Features**
- **20 Realistic Products** - Apple, Dell, Logitech, and other popular brands
- **Varied Stock Levels** - Some products with low stock for testing alerts
- **Multiple Categories** - Electronics, Furniture, Kitchen, Gaming, Office, Accessories
- **Realistic Pricing** - Market-appropriate prices and descriptions
- **Complete Data** - All required fields including SKU, description, price, stock levels

### **Loading Sample Data**

#### **Option 1: Interactive Menu (Recommended)**
```bash
./update_sample_data.sh
```
This provides a menu with options to:
- Load via API (recommended for running app)
- Load via direct database access
- View current sample data structure
- Check current database status

#### **Option 2: API-based Loading**
```bash
# Make sure API is running
kubectl port-forward service/flask-service 5000:5000 &

# Load sample data via API
python3 load_via_api.py
```
**Benefits:**
- Respects API validation rules
- Works with running application
- Handles rate limiting
- Better error handling

#### **Option 3: Direct Database Access**
```bash
python3 load_sample_data.py
```
**Use when:**
- API is not running
- Need direct database access
- Bulk data operations

#### **Option 4: Shell Script Wrapper**
```bash
./setup_sample_data.sh
```
**Features:**
- Checks dependencies
- Validates database connection
- Provides status updates
- Checks if services are running

### **Sample Data Structure**
```json
{
  "products": [
    {
      "name": "MacBook Pro 14-inch",
      "sku": "APPLE001",
      "description": "Apple MacBook Pro with M3 chip, 14-inch display",
      "price": 1999.99,
      "stock_level": 15,
      "min_stock_threshold": 5,
      "category": "Electronics"
    }
  ]
}
```

### **Sample Products Included**
1. **Electronics**: MacBook Pro, iPhone 15 Pro, AirPods Pro, iPad Air, Dell Monitor
2. **Gaming**: Mechanical Keyboard RGB, Gaming Mouse Pad
3. **Furniture**: Office Chair Premium, Standing Desk
4. **Kitchen**: Coffee Machine Espresso
5. **Office**: Desk Lamp LED, USB-C Hub
6. **Accessories**: Phone Case, Power Bank, External SSD

### **Testing Scenarios**
The sample data includes various scenarios for testing:
- **Low Stock Alerts**: AirPods Pro (3 units, threshold 15)
- **Out of Stock**: Standing Desk (0 units)
- **Normal Stock**: MacBook Pro (15 units, threshold 5)
- **High Stock**: Gaming Mouse Pad (30 units, threshold 20)

### **Updating Sample Data**
1. **Edit the JSON file**:
   ```bash
   # Edit sample_products.json
   nano sample_products.json
   # or
   code sample_products.json
   ```

2. **Reload the data**:
   ```bash
   # Use interactive menu
   ./update_sample_data.sh
   
   # Or direct API loading
   python3 load_via_api.py
   ```

3. **Verify the changes**:
   ```bash
   # Check via API
   curl http://localhost:5000/api/products
   
   # Check analytics
   curl http://localhost:5000/api/products/analytics
   ```

### **Sample Data for Grafana Dashboards**
The sample data provides excellent metrics for Grafana dashboards:
- **Stock Level Variations** - Different stock levels for trend analysis
- **Category Distribution** - Multiple categories for filtering
- **Price Ranges** - Various price points for financial analysis
- **Low Stock Scenarios** - Perfect for testing alert systems

### **Quick Data Reset**
To quickly reset and reload sample data:
```bash
# Clear and reload
./update_sample_data.sh
# Choose option 1 (API loading)
# When prompted, choose option 2 (clear database)
```

---

## 📊 Monitoring & Analytics

### **Grafana Dashboards**
- **API Performance**: Response times, request rates, error rates
- **Business Metrics**: Stock levels, low stock alerts, restock operations
- **System Health**: CPU, memory, container metrics

### **Key Metrics**
- `http_requests_total` - Request count by endpoint/status
- `http_request_duration_seconds` - Response latency
- `product_stock_level` - Current stock levels
- `low_stock_alerts_total` - Low stock alerts
- `restock_operations_total` - Restock operations
- `product_operations_total` - CRUD operations by type

### **Prometheus Queries**
```promql
# Average response time
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))

# Request rate
sum(rate(http_requests_total[5m])) by (endpoint)

# Current stock levels
product_stock_level

# Low stock alerts in last hour
sum(increase(low_stock_alerts_total[1h]))

# Restock operations in last hour
sum(increase(restock_operations_total[1h]))
```

### **Monitoring Setup**
```bash
# Deploy monitoring stack
kubectl apply -f k8s/monitoring/

# Access Grafana
kubectl port-forward service/grafana-service 3001:3000
# Login: admin/admin123

# Access Prometheus
kubectl port-forward service/prometheus-service 9090:9090
```

---

## 🛡️ Security Features

### **Input Validation**
- SKU format validation (3-20 alphanumeric chars)
- Price validation (positive numbers)
- Stock level validation (non-negative integers)
- String length limits (name: 255 chars, description: 1000 chars)

### **Rate Limiting**
- Default: 200 requests/day, 50/hour
- Create product: 10/minute
- Restock: 20/minute

### **Security Headers**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`

### **Container Security**
- Non-root user execution
- Read-only filesystem (except /tmp)
- Dropped capabilities
- Resource limits

---

## 📁 Project Structure

```
smart-retail-app/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Development setup
├── init.sql                # Database initialization
├── frontend/               # React frontend
│   ├── src/
│   ├── package.json
│   └── public/
├── k8s/                    # Kubernetes manifests
│   ├── configs/
│   ├── secrets/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── monitoring/
├── test_api.py             # API testing script
├── health_check.py         # Health check tool
├── test_monitoring.py      # Load testing
├── deploy_with_health_check.sh # Deployment script
├── COMPLETE_GUIDE.md       # This file
├── TESTING_GUIDE.md        # Testing guide
├── CODE_REVIEW_SUMMARY.md  # Development history
└── README.md               # Basic project info
```

---

## 🔍 Health Checks

### **Automated Health Check**
```bash
python3 health_check.py
```

### **Manual Health Checks**
```bash
# API health
curl http://localhost:5000/api/health

# Database connection
curl http://localhost:5000/api/products

# Metrics endpoint
curl http://localhost:5000/metrics

# Pod status
kubectl get pods

# Service status
kubectl get services
```

### **Logs**
```bash
# Backend logs
kubectl logs -f deployment/flask-deployment

# Database logs
kubectl logs -f deployment/postgres-deployment

# Monitoring logs
kubectl logs -f deployment/prometheus
kubectl logs -f deployment/grafana
```

---

## 🧪 Testing

For comprehensive testing information, see **[TESTING_GUIDE.md](TESTING_GUIDE.md)** which includes:
- Manual testing checklist
- Automated testing scripts
- End-to-end testing
- Load testing
- Troubleshooting guide

---

## 🚨 Troubleshooting

### **Common Issues**

#### **Pod in CrashLoopBackOff**
```bash
# Check logs
kubectl logs <pod-name>

# Check pod description
kubectl describe pod <pod-name>

# Restart deployment
kubectl rollout restart deployment/flask-deployment
```

#### **Database Connection Issues**
```bash
# Check PostgreSQL pod
kubectl get pods -l component=database

# Check database logs
kubectl logs deployment/postgres-deployment

# Test database connection
kubectl exec -it postgres-deployment-<pod-id> -- psql -U inventory_user -d inventory_db
```

#### **Port Forwarding Issues**
```bash
# Kill existing port forwards
pkill -f "kubectl port-forward"

# Start fresh port forwarding
kubectl port-forward service/flask-service 5000:5000 &
```

#### **Monitoring Not Working**
```bash
# Check Prometheus targets
kubectl port-forward service/prometheus-service 9090:9090
# Visit http://localhost:9090/targets

# Check Grafana datasource
kubectl port-forward service/grafana-service 3001:3000
# Login and check Prometheus datasource
```

---

## 📈 Performance Optimization

### **Database Optimization**
- Connection pooling configured
- Indexes on frequently queried fields
- Efficient queries with SQLAlchemy

### **API Optimization**
- Rate limiting to prevent abuse
- Input validation to prevent errors
- Efficient error handling

### **Container Optimization**
- Resource limits configured
- Health checks implemented
- Security best practices

---

## 🔄 Development Workflow

### **Making Changes**
1. Update code in `app.py`
2. Build new Docker image
3. Push to registry
4. Deploy to Kubernetes
5. Run health checks

### **Testing Changes**
1. Run `python3 health_check.py`
2. Run `python3 test_monitoring.py`
3. Check Grafana dashboards
4. Verify API endpoints

### **Monitoring Changes**
1. Check Prometheus targets
2. Verify metrics collection
3. Review Grafana dashboards
4. Check application logs

---

## 📞 Support

### **Documentation Files**
- **COMPLETE_GUIDE.md** - This comprehensive guide
- **TESTING_GUIDE.md** - Testing and verification
- **CODE_REVIEW_SUMMARY.md** - Development history
- **README.md** - Basic project information

### **Useful Commands**
```bash
# Quick status check
kubectl get all

# View all logs
kubectl logs -f deployment/flask-deployment

# Health check
python3 health_check.py

# Load test
python3 test_monitoring.py
```

---

## 🎉 Success Criteria

Your Smart Retail App is **fully operational** when:
- ✅ All pods are running (1/1 Ready)
- ✅ API responds to health checks
- ✅ Database connection works
- ✅ Frontend loads without errors
- ✅ Monitoring shows real-time metrics
- ✅ All automated tests pass
- ✅ Security features are active

**Congratulations!** 🎉 Your production-ready inventory management system is complete! 