#!/bin/bash

# Quick start script for Inventory Management System
# This script helps you get the application up and running quickly

set -e  # Exit on any error

echo "🚀 Inventory Management System Setup"
echo "====================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. You can modify it if needed."
else
    echo "✅ .env file already exists"
fi

# Check if containers are already running
if docker-compose ps | grep -q "Up"; then
    echo "⚠️  Some containers are already running"
    read -p "Do you want to restart them? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Stopping existing containers..."
        docker-compose down
    fi
fi

# Build and start containers
echo "🏗️  Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are healthy
echo "🔍 Checking service health..."

# Check database
if docker-compose exec -T db pg_isready -U inventory_user -d inventory_db >/dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready"
    echo "📋 Database logs:"
    docker-compose logs db
    exit 1
fi

# Check backend API
if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
    echo "✅ Backend API is ready"
else
    echo "⏳ Waiting for backend API..."
    sleep 15
    if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
        echo "✅ Backend API is now ready"
    else
        echo "❌ Backend API is not responding"
        echo "📋 Backend logs:"
        docker-compose logs backend
        exit 1
    fi
fi

# Display status
echo ""
echo "🎉 Application is ready!"
echo "======================="
echo ""
echo "🌐 API Base URL: http://localhost:5000"
echo "🏥 Health Check: http://localhost:5000/api/health"
echo "🗄️  pgAdmin: http://localhost:8080 (admin@inventory.com / admin123)"
echo ""
echo "📚 Available endpoints:"
echo "  GET    /api/products              - List all products"
echo "  POST   /api/products              - Create new product"
echo "  GET    /api/products/{id}         - Get specific product"
echo "  PUT    /api/products/{id}         - Update product"
echo "  DELETE /api/products/{id}         - Delete product"
echo "  POST   /api/products/{id}/restock - Restock product"
echo "  GET    /api/restocks              - Get restock history"
echo "  GET    /api/products/low-stock    - Get low stock products"
echo "  GET    /api/products/analytics    - Get analytics"
echo ""
echo "🧪 To test the API:"
echo "  python3 test_api.py"
echo ""
echo "📊 To view logs:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f db"
echo ""
echo "🛑 To stop the application:"
echo "  docker-compose down"
echo ""

# Ask if user wants to run tests
read -p "Do you want to run API tests now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command_exists python3; then
        echo "🧪 Running API tests..."
        python3 test_api.py
    else
        echo "❌ Python 3 is not installed. Please install Python 3 to run tests."
        echo "You can test manually using curl or Postman."
    fi
fi

echo ""
echo "✅ Setup complete! Your inventory management system is running."
echo "Happy coding! 🎉"