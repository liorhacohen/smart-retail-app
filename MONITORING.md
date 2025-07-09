# Monitoring Setup for Smart Retail App

This document describes the monitoring setup using Prometheus and Grafana for the Smart Retail Inventory Management System.

## Overview

The monitoring stack consists of:
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Custom Metrics**: Business-specific metrics from the Flask API

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask API     │    │   Prometheus    │    │     Grafana     │
│                 │    │                 │    │                 │
│ /metrics        │───▶│   Scrapes       │───▶│   Dashboards    │
│ endpoint        │    │   metrics       │    │   & Alerts      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Metrics Collected

### API Metrics
- **HTTP Request Duration**: Response times for all API endpoints
- **HTTP Request Count**: Total requests by endpoint and status code
- **Request Rate**: Requests per second

### Business Metrics
- **Product Stock Levels**: Current stock for each product
- **Low Stock Alerts**: Count of low stock alerts triggered
- **Restock Operations**: Number of restock operations performed
- **Product Operations**: Create, update, delete operations

### Container Metrics
- **CPU Usage**: Container CPU utilization
- **Memory Usage**: Container memory consumption
- **Resource Limits**: Resource requests and limits

## Deployment

### Prerequisites
- Kubernetes cluster running
- kubectl configured
- Ingress controller (optional, for external access)

### Quick Deployment
```bash
# Deploy the entire monitoring stack
./deploy_monitoring.sh
```

### Manual Deployment
```bash
# Create namespace
kubectl create namespace monitoring

# Deploy Prometheus
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml

# Deploy Grafana
kubectl apply -f k8s/monitoring/grafana-datasources.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml

# Deploy Ingress (optional)
kubectl apply -f k8s/monitoring/monitoring-ingress.yaml
```

## Access

### Grafana
- **URL**: http://grafana.local (with ingress) or port-forward
- **Username**: admin
- **Password**: admin123
- **Port-forward**: `kubectl port-forward -n monitoring svc/grafana-service 3000:3000`

### Prometheus
- **URL**: http://prometheus.local (with ingress) or port-forward
- **Port-forward**: `kubectl port-forward -n monitoring svc/prometheus-service 9090:9090`

## Dashboards

### Inventory Management Dashboard
The main dashboard includes:

1. **API Response Times**
   - 95th and 50th percentile response times
   - Broken down by endpoint

2. **HTTP Request Rate**
   - Requests per second by endpoint
   - Real-time traffic monitoring

3. **HTTP Status Codes**
   - Success vs error rates
   - Status code distribution

4. **Product Stock Levels**
   - Current stock levels for all products
   - Visual representation of inventory

5. **Business Metrics**
   - Low stock alerts (last hour)
   - Restock operations (last hour)
   - Product operations by type

6. **Container Resources**
   - CPU usage percentage
   - Memory usage in MB
   - Resource utilization trends

## Custom Metrics

### Available Prometheus Queries

#### API Performance
```promql
# Average response time by endpoint
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))

# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Error rate
sum(rate(http_requests_total{status=~"4..|5.."}[5m])) by (endpoint)
```

#### Business Metrics
```promql
# Current stock levels
product_stock_level

# Low stock alerts in last hour
sum(increase(low_stock_alerts_total[1h]))

# Restock operations in last hour
sum(increase(restock_operations_total[1h]))

# Product operations by type
sum(increase(product_operations_total[1h])) by (operation_type)
```

#### Container Metrics
```promql
# CPU usage percentage
rate(container_cpu_usage_seconds_total{container=~"flask-backend.*"}[5m]) * 100

# Memory usage in MB
container_memory_usage_bytes{container=~"flask-backend.*"} / 1024 / 1024
```

## Configuration

### Prometheus Configuration
Located in `k8s/monitoring/prometheus-configmap.yaml`:
- Scrape interval: 15s
- Flask API scrape interval: 10s
- Kubernetes pod discovery enabled
- Node metrics collection enabled

### Grafana Configuration
- **Datasource**: Prometheus (auto-configured)
- **Dashboards**: Pre-configured inventory dashboard
- **Authentication**: Basic auth (admin/admin123)

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n monitoring
kubectl describe pod <pod-name> -n monitoring
```

### Check Logs
```bash
# Prometheus logs
kubectl logs -f deployment/prometheus -n monitoring

# Grafana logs
kubectl logs -f deployment/grafana -n monitoring
```

### Verify Metrics Endpoint
```bash
# Port-forward to Flask service
kubectl port-forward svc/flask-service 5000:5000

# Check metrics endpoint
curl http://localhost:5000/metrics
```

### Common Issues

1. **Prometheus can't scrape Flask metrics**
   - Verify Flask pod has correct annotations
   - Check if `/metrics` endpoint is accessible
   - Ensure network connectivity

2. **Grafana can't connect to Prometheus**
   - Verify Prometheus service is running
   - Check datasource configuration
   - Ensure both pods are in same namespace

3. **No metrics appearing**
   - Check if Flask app is generating metrics
   - Verify Prometheus configuration
   - Check scrape targets in Prometheus UI

## Scaling and Production

### Resource Requirements
- **Prometheus**: 512Mi RAM, 250m CPU (requests)
- **Grafana**: 256Mi RAM, 100m CPU (requests)
- **Storage**: 10Gi for Prometheus, 5Gi for Grafana

### High Availability
- Consider running multiple Prometheus replicas
- Use persistent volumes for data retention
- Implement backup strategies for dashboards

### Security
- Change default passwords
- Use RBAC for access control
- Consider TLS termination
- Implement network policies

## Maintenance

### Data Retention
- Prometheus data retention: 200 hours (configurable)
- Consider long-term storage solutions for historical data

### Updates
- Monitor for security updates
- Test updates in staging environment
- Backup dashboards before updates

### Monitoring the Monitoring
- Set up alerts for Prometheus/Grafana availability
- Monitor resource usage of monitoring stack
- Regular health checks of the monitoring system 