# 🚀 Quick Deployment Guide

## Option 1: Automated Deployment (Recommended)
```bash
chmod +x deploy_monitoring.sh
./deploy_monitoring.sh
```

## Option 2: Manual Step-by-Step
```bash
# 1. Deploy Prometheus
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml

# 2. Deploy Grafana  
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/grafana-dashboards.yaml

# 3. Setup ingress
kubectl apply -f k8s/monitoring/monitoring-ingress.yaml

# 4. Update Flask deployment
kubectl apply -f k8s/deployments/flask-deployment.yaml

# 5. Start tunnel (separate terminal)
minikube tunnel

# 6. Test monitoring
python3 scripts/test_monitoring.py
```

## Access URLs
- **Grafana**: http://localhost/grafana/ (admin/inventory123)
- **Prometheus**: http://localhost/prometheus/
- **Main App**: http://localhost/
- **Metrics**: http://localhost/metrics
