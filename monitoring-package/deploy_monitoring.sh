#!/bin/bash

# 🚀 Monitoring Stack Deployment Script
set -e

echo "🚀 Deploying Monitoring Stack for Inventory Management"
echo "====================================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed"
    exit 1
fi

if ! command -v minikube &> /dev/null; then
    echo "❌ minikube is not installed"
    exit 1
fi

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "❌ Minikube is not running. Start it with: minikube start"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check if base application is deployed
if ! kubectl get deployment flask-deployment &> /dev/null; then
    echo "⚠️ Flask deployment not found. Make sure your base application is deployed first."
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Deploy monitoring stack
echo "📊 Deploying Prometheus..."
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml

echo "📈 Deploying Grafana..."
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml

echo "🌐 Setting up ingress..."
kubectl apply -f k8s/monitoring/monitoring-ingress.yaml

echo "🔄 Updating Flask deployment with monitoring annotations..."
kubectl apply -f k8s/deployments/flask-deployment.yaml

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=monitoring --timeout=300s

echo "🔍 Checking deployment status..."
kubectl get pods -l app=monitoring
kubectl get pods -l app=inventory-management

echo ""
echo "✅ Monitoring stack deployed successfully!"
echo ""
echo "📊 Access URLs:"
echo "  Main App:    http://localhost/"
echo "  Prometheus:  http://localhost/prometheus/"
echo "  Grafana:     http://localhost/grafana/ (admin/inventory123)"
echo "  Metrics:     http://localhost/metrics"
echo ""
echo "🚨 IMPORTANT: Make sure 'minikube tunnel' is running in another terminal!"
echo ""
echo "🧪 To test monitoring:"
echo "  python3 scripts/test_monitoring.py"
