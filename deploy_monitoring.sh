#!/bin/bash

# Deploy Monitoring Stack for Smart Retail App
# This script deploys Prometheus and Grafana for monitoring

set -e

echo "🚀 Deploying Monitoring Stack..."

# Create monitoring namespace if it doesn't exist
echo "📦 Creating monitoring namespace..."
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Deploy Prometheus
echo "📊 Deploying Prometheus..."
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml

# Deploy Grafana
echo "📈 Deploying Grafana..."
kubectl apply -f k8s/monitoring/grafana-datasources.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml

# Deploy Ingress (optional - comment out if not using ingress controller)
echo "🌐 Deploying Ingress..."
kubectl apply -f k8s/monitoring/monitoring-ingress.yaml

# Wait for pods to be ready
echo "⏳ Waiting for monitoring pods to be ready..."
kubectl wait --for=condition=ready pod -l app=monitoring,component=prometheus -n monitoring --timeout=300s
kubectl wait --for=condition=ready pod -l app=monitoring,component=grafana -n monitoring --timeout=300s

# Get service information
echo "📋 Monitoring Stack Deployment Complete!"
echo ""
echo "🔍 Access Information:"
echo "Grafana:"
echo "  - URL: http://grafana.local (if using ingress)"
echo "  - Username: admin"
echo "  - Password: admin123"
echo "  - Port-forward: kubectl port-forward -n monitoring svc/grafana-service 3000:3000"
echo ""
echo "Prometheus:"
echo "  - URL: http://prometheus.local (if using ingress)"
echo "  - Port-forward: kubectl port-forward -n monitoring svc/prometheus-service 9090:9090"
echo ""
echo "📊 Available Metrics:"
echo "  - API Response Times: http_request_duration_seconds"
echo "  - Request Count: http_requests_total"
echo "  - Stock Levels: product_stock_level"
echo "  - Low Stock Alerts: low_stock_alerts_total"
echo "  - Restock Operations: restock_operations_total"
echo "  - Product Operations: product_operations_total"
echo ""
echo "🎯 Next Steps:"
echo "1. Access Grafana and log in with admin/admin123"
echo "2. The 'Inventory Management Dashboard' should be automatically available"
echo "3. Verify that Prometheus is scraping metrics from your Flask app"
echo "4. Customize dashboards as needed" 