# 📊 Inventory Management System - Monitoring Package

This package adds comprehensive **Prometheus** and **Grafana** monitoring to your Kubernetes inventory management system.

## 🎯 What This Adds

- **📊 Prometheus**: Metrics collection and alerting
- **📈 Grafana**: Beautiful dashboards and visualizations  
- **🔍 API Monitoring**: Response times, request rates, error tracking
- **📦 Business Metrics**: Stock levels, inventory value, restocking activity
- **🖥️ Infrastructure Monitoring**: CPU, memory, container health

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites Check
```bash
# Ensure you have these installed:
kubectl version --client
minikube version  
docker version

# Your base inventory app should already be deployed
kubectl get deployment flask-deployment
```

### 2. Deploy Monitoring Stack
```bash
# Make the script executable and run it
chmod +x deploy_monitoring.sh
./deploy_monitoring.sh
```

### 3. Start Access Tunnel
```bash
# In a separate terminal, keep this running:
minikube tunnel
```

### 4. Access Your Dashboards
- **📊 Grafana Dashboard**: http://localhost/grafana/ 
  - Username: `admin`
  - Password: `inventory123`
- **📈 Prometheus**: http://localhost/prometheus/
- **🔧 Raw Metrics**: http://localhost/metrics

### 5. Test Everything
```bash
python3 scripts/test_monitoring.py
```

## 📁 Package Contents

```
monitoring-package/
├── deploy_monitoring.sh           # One-click deployment
├── k8s/
│   ├── monitoring/
│   │   ├── prometheus-configmap.yaml     # Prometheus config & alerts
│   │   ├── prometheus-deployment.yaml    # Prometheus deployment
│   │   ├── grafana-deployment.yaml       # Grafana with dashboards
│   │   ├── grafana-dashboards.yaml       # Pre-built dashboards
│   │   └── monitoring-ingress.yaml       # External access
│   └── deployments/
│       └── flask-deployment.yaml         # Updated with metrics
├── scripts/
│   └── test_monitoring.py               # Test & validation
├── requirements.txt                      # Updated Python deps
└── docs/
    └── README.md                         # This file
```

## 🎨 Dashboard Features

Your Grafana dashboard includes:

### **Performance Metrics**
- API response times (50th, 95th, 99th percentiles)
- Request rates by endpoint
- Error rates and exceptions
- Request volume trends

### **Business Intelligence** 
- Total products count
- Inventory value in real-time
- Stock status distribution
- Low stock alerts
- Recent restocking activity

### **Infrastructure Health**
- Container CPU and memory usage
- Pod health and availability
- Resource utilization trends

## 🔧 Updating Your Flask App

**If you haven't updated your Flask app yet**, you need to:

1. **Add Prometheus client**:
   ```bash
   pip install prometheus-client==0.17.1
   ```

2. **Update your `app.py`** with the enhanced version that includes:
   - Prometheus metrics collection
   - `/metrics` endpoint
   - Request timing and counting
   - Business metrics (stock levels, inventory value)

3. **Rebuild and deploy**:
   ```bash
   docker build -t your-username/smart-retail-app:v2 .
   docker push your-username/smart-retail-app:v2
   kubectl set image deployment/flask-deployment flask-backend=your-username/smart-retail-app:v2
   ```

## 📊 Available Metrics

### **API Metrics**
- `flask_request_total` - Total HTTP requests
- `flask_request_duration_seconds` - Request response times
- `flask_request_exceptions_total` - Request errors

### **Business Metrics**
- `inventory_total_products` - Total products count
- `inventory_total_value` - Total inventory value ($)
- `inventory_low_stock_products` - Products below threshold
- `inventory_out_of_stock_products` - Products with zero stock
- `inventory_recent_restocks` - Restocks in last 7 days

### **Infrastructure Metrics**
- `container_cpu_usage_seconds_total` - CPU usage
- `container_memory_usage_bytes` - Memory usage

## 🚨 Built-in Alerts

Prometheus automatically alerts on:
- High API response times (>1 second)
- High error rates (>10%)
- Multiple low stock products (>5)
- Service downtime

## 🧪 Testing Your Setup

### **Generate Traffic**
```bash
# Run the test script to generate metrics
python3 scripts/test_monitoring.py

# Or manually create some products
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "sku": "TEST001", "stock_level": 5, "price": 99.99}'
```

### **Check Metrics**
```bash
# View raw metrics
curl http://localhost/metrics | grep inventory

# Check Prometheus targets
curl http://localhost/prometheus/api/v1/targets

# Query specific metrics
curl 'http://localhost/prometheus/api/v1/query?query=flask_request_total'
```

## 🔧 Troubleshooting

### **Metrics Not Appearing**
```bash
# Check Flask deployment
kubectl logs deployment/flask-deployment

# Verify metrics endpoint
kubectl port-forward deployment/flask-deployment 5000:5000
curl http://localhost:5000/metrics

# Check Prometheus
kubectl logs deployment/prometheus
```

### **Cannot Access Dashboards**
```bash
# Ensure tunnel is running
minikube tunnel

# Check ingress
kubectl get ingress

# Alternative: use port forwarding
kubectl port-forward svc/grafana-service 3000:3000
# Then access: http://localhost:3000
```

### **Pods Not Starting**
```bash
# Check pod status
kubectl get pods -l app=monitoring

# Check specific pod
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

## 📈 Custom Queries

Use these Prometheus queries in Grafana:

```promql
# Average response time
avg(rate(flask_request_duration_seconds_sum[5m]) / rate(flask_request_duration_seconds_count[5m]))

# Request rate by endpoint  
sum(rate(flask_request_total[5m])) by (endpoint)

# Error percentage
100 * (rate(flask_request_exceptions_total[5m]) / rate(flask_request_total[5m]))

# Stock distribution
inventory_in_stock_products + inventory_low_stock_products + inventory_out_of_stock_products
```

## 🎯 What's Next?

### **Add More Metrics**
Extend your Flask app with custom business metrics:
```python
PRODUCT_VIEWS = Counter('product_views_total', 'Product page views', ['product_id'])
SALES_VALUE = Histogram('sales_value_dollars', 'Sales transaction values')
```

### **Set Up Alerting**
Configure Grafana to send alerts via email/Slack when issues occur.

### **Production Deployment**
- Add persistent storage for Prometheus data
- Set up authentication for Grafana
- Configure external monitoring endpoints

## 🎉 Success!

You now have:
- ✅ Real-time API performance monitoring
- ✅ Business intelligence dashboards
- ✅ Automated alerting on issues  
- ✅ Infrastructure health monitoring
- ✅ Production-ready observability

Your inventory management system is now **enterprise-ready** with comprehensive monitoring! 🚀
