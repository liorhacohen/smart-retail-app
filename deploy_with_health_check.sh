#!/bin/bash

# Deployment script with health checks for Smart Retail App
set -e

echo "🚀 Starting deployment with health checks..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="litalhay/smart-retail-app"
TAG="latest"
NAMESPACE="default"

echo -e "${YELLOW}📦 Building and pushing Docker image...${NC}"
docker build -t ${IMAGE_NAME}:${TAG} .
docker push ${IMAGE_NAME}:${TAG}

echo -e "${YELLOW}🔧 Deploying to Kubernetes...${NC}"
kubectl apply -f k8s/configs/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/services/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/ingress/

echo -e "${YELLOW}⏳ Waiting for deployments to be ready...${NC}"
kubectl rollout status deployment/flask-deployment --timeout=300s
kubectl rollout status deployment/postgres-deployment --timeout=300s

echo -e "${YELLOW}🔍 Setting up port forwarding...${NC}"
# Kill existing port forwards
pkill -f "kubectl port-forward" || true

# Start port forwarding in background
kubectl port-forward service/flask-service 5000:5000 &
kubectl port-forward service/grafana-service 3001:3000 &
kubectl port-forward service/prometheus-service 9090:9090 &

# Wait for port forwarding to be ready
sleep 10

echo -e "${YELLOW}🏥 Running health checks...${NC}"
python3 health_check.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Health checks passed!${NC}"
else
    echo -e "${RED}❌ Health checks failed!${NC}"
    echo -e "${YELLOW}🔍 Checking pod status...${NC}"
    kubectl get pods
    kubectl logs deployment/flask-deployment --tail=50
    exit 1
fi

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📊 Access URLs:${NC}"
echo -e "   Frontend: http://localhost:3000"
echo -e "   Grafana: http://localhost:3001 (admin/admin123)"
echo -e "   Prometheus: http://localhost:9090"
echo -e "   API: http://localhost:5000"
echo ""
echo -e "${YELLOW}🧪 Run tests:${NC}"
echo -e "   python3 test_monitoring.py"
echo -e "   python3 health_check.py"
echo ""
echo -e "${YELLOW}📝 View logs:${NC}"
echo -e "   kubectl logs -f deployment/flask-deployment" 