#!/bin/bash

# Smart Retail App CI/CD Pipeline Setup Script
# This script helps you set up the CI/CD pipeline quickly

set -e

echo "🚀 Smart Retail App CI/CD Pipeline Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running in the correct directory
if [ ! -f "backend/app.py" ] || [ ! -f "backend/requirements.txt" ]; then
    print_error "Please run this script from the root directory of your Smart Retail App project"
    exit 1
fi

print_status "Starting CI/CD pipeline setup..."

# Step 1: Install development dependencies
print_info "Installing development dependencies..."

# Determine the correct pip command
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
elif command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif python3 -m pip --version &> /dev/null; then
    PIP_CMD="python3 -m pip"
else
    print_error "No pip installation found. Please install pip first."
    exit 1
fi

print_info "Using pip command: $PIP_CMD"

if [ -f "backend/requirements-dev.txt" ]; then
    $PIP_CMD install -r backend/requirements-dev.txt
    print_status "Development dependencies installed"
else
    print_warning "backend/requirements-dev.txt not found, installing basic testing dependencies..."
    $PIP_CMD install pytest pytest-cov pytest-mock flake8 black isort
fi

# Step 2: Install frontend dependencies
print_info "Installing frontend dependencies..."
if [ -d "frontend" ]; then
    cd frontend
    npm install
    npm install --save-dev eslint eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y
    cd ..
    print_status "Frontend dependencies installed"
else
    print_warning "Frontend directory not found"
fi

# Step 3: Run initial linting check
print_info "Running initial code quality checks..."
if command -v flake8 &> /dev/null; then
    flake8 backend/ --count --select=E9,F63,F7,F82 --show-source --statistics || print_warning "Some linting issues found"
    print_status "Python linting completed"
else
    print_warning "flake8 not found, skipping Python linting"
fi

if command -v black &> /dev/null; then
    black --check backend/ || print_warning "Code formatting issues found (run 'black backend/' to fix)"
    print_status "Code formatting check completed"
else
    print_warning "black not found, skipping code formatting check"
fi

# Step 4: Run initial tests
print_info "Running initial tests..."
if command -v pytest &> /dev/null; then
    pytest backend/tests/ -v --tb=short || print_warning "Some tests failed"
    print_status "Backend tests completed"
else
    print_warning "pytest not found, skipping backend tests"
fi

# Step 5: Check Docker setup
print_info "Checking Docker setup..."
if command -v docker &> /dev/null; then
    docker --version
    print_status "Docker is available"
    
    # Test Docker build
    print_info "Testing Docker build..."
    if docker build -t smart-retail-test ./backend > /dev/null 2>&1; then
        print_status "Docker build successful"
        docker rmi smart-retail-test > /dev/null 2>&1
    else
        print_warning "Docker build failed - check your Dockerfile"
    fi
else
    print_warning "Docker not found - install Docker to use containerization"
fi

# Step 6: Check Kubernetes setup
print_info "Checking Kubernetes setup..."
if command -v kubectl &> /dev/null; then
    kubectl version --client
    print_status "kubectl is available"
    
    # Check if cluster is accessible
    if kubectl cluster-info &> /dev/null; then
        print_status "Kubernetes cluster is accessible"
    else
        print_warning "Kubernetes cluster not accessible - check your kubeconfig"
    fi
else
    print_warning "kubectl not found - install kubectl to use Kubernetes deployment"
fi

# Step 7: Create GitHub Secrets template
print_info "Creating GitHub Secrets template..."
cat > github-secrets-template.txt << 'EOF'
# GitHub Repository Secrets Template
# Add these secrets in your GitHub repository:
# Settings → Secrets and variables → Actions

# Docker Hub credentials
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_access_token

# Kubernetes cluster access (base64 encoded kubeconfig)
KUBE_CONFIG_DATA=$(cat ~/.kube/config | base64 -w 0)

# Application URLs
API_BASE_URL=https://your-app-domain.com

# Notifications (optional)
SLACK_WEBHOOK=https://hooks.slack.com/services/...

# Instructions:
# 1. Replace the values above with your actual credentials
# 2. Go to your GitHub repository settings
# 3. Navigate to Secrets and variables → Actions
# 4. Add each secret with the exact name and value
EOF

print_status "GitHub secrets template created: github-secrets-template.txt"

# Step 8: Create local test script
print_info "Creating local test script..."
cat > test-pipeline-local.sh << 'EOF'
#!/bin/bash

# Local CI/CD Pipeline Test Script
echo "🧪 Testing CI/CD pipeline locally..."

# Test linting
echo "1. Testing code linting..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Test formatting
echo "2. Testing code formatting..."
black --check --diff .
isort --check-only --diff .

# Test backend
echo "3. Testing backend..."
pytest tests/ -v --cov=app --cov-report=term-missing

# Test frontend (if available)
if [ -d "frontend" ]; then
    echo "4. Testing frontend..."
    cd frontend
    npm run lint || echo "Linting issues found"
    npm test -- --coverage --watchAll=false --passWithNoTests || echo "Tests completed"
    cd ..
fi

# Test Docker build
echo "5. Testing Docker build..."
docker build -t smart-retail-test .
docker rmi smart-retail-test

echo "✅ Local pipeline test completed!"
EOF

chmod +x test-pipeline-local.sh
print_status "Local test script created: test-pipeline-local.sh"

# Step 9: Create deployment checklist
print_info "Creating deployment checklist..."
cat > deployment-checklist.md << 'EOF'
# Deployment Checklist

## Pre-Deployment
- [ ] All tests pass locally
- [ ] Code is linted and formatted
- [ ] Docker images build successfully
- [ ] Kubernetes manifests are valid
- [ ] GitHub secrets are configured

## Deployment Steps
1. [ ] Push code to main branch
2. [ ] Monitor GitHub Actions pipeline
3. [ ] Verify all stages pass
4. [ ] Check application health
5. [ ] Run API tests against live deployment
6. [ ] Verify monitoring is working
7. [ ] Test application functionality

## Post-Deployment
- [ ] Monitor application logs
- [ ] Check Prometheus metrics
- [ ] Verify Grafana dashboards
- [ ] Test all API endpoints
- [ ] Monitor resource usage
- [ ] Send deployment notification

## Rollback Plan
- [ ] Keep previous version ready
- [ ] Document rollback procedure
- [ ] Test rollback process
EOF

print_status "Deployment checklist created: deployment-checklist.md"

# Step 10: Summary
echo ""
echo "🎉 CI/CD Pipeline Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Review github-secrets-template.txt and configure GitHub secrets"
echo "2. Run ./test-pipeline-local.sh to test locally"
echo "3. Push your code to trigger the pipeline"
echo "4. Monitor the GitHub Actions tab"
echo ""
echo "Files created:"
echo "- github-secrets-template.txt (GitHub secrets configuration)"
echo "- test-pipeline-local.sh (Local testing script)"
echo "- deployment-checklist.md (Deployment checklist)"
echo ""
echo "Documentation:"
echo "- CI_CD_SETUP_GUIDE.md (Comprehensive setup guide)"
echo "- README.md (Project documentation)"
echo ""
print_status "Setup completed successfully!" 