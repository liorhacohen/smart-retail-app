#!/bin/bash

# Local CI/CD Pipeline Test Script
echo "🧪 Testing CI/CD pipeline locally..."

# Test linting
echo "1. Testing code linting..."
flake8 backend/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 backend/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Test formatting
echo "2. Testing code formatting..."
black --check --diff backend/
isort --check-only --diff backend/

# Test backend
echo "3. Testing backend..."
pytest backend/tests/ -v --cov=backend.app --cov-report=term-missing

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
docker build -t smart-retail-test ./backend
docker rmi smart-retail-test

echo "✅ Local pipeline test completed!"
