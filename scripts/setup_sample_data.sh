#!/bin/bash

# Inventory Management System - Sample Data Setup
# This script loads sample products into your local database

echo "🚀 Inventory Management - Sample Data Setup"
echo "=================================================="

# Check if sample_products.json exists
if [ ! -f "sample_products.json" ]; then
    echo "❌ Error: sample_products.json not found!"
    echo "   Please make sure the JSON file is in the current directory."
    exit 1
fi

# Check if Python script exists
if [ ! -f "load_sample_data.py" ]; then
    echo "❌ Error: load_sample_data.py not found!"
    echo "   Please make sure the Python script is in the current directory."
    exit 1
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL connection..."
if ! psql -U inventory_user -d inventory_db -c "SELECT 1;" >/dev/null 2>&1; then
    echo "❌ Error: Cannot connect to PostgreSQL database!"
    echo "   Please make sure:"
    echo "   1. PostgreSQL is running"
    echo "   2. Database 'inventory_db' exists"
    echo "   3. User 'inventory_user' has access"
    exit 1
fi

echo "✅ Database connection successful!"

# Check if Python dependencies are installed
echo "🔍 Checking Python dependencies..."
if ! python3 -c "import psycopg2" >/dev/null 2>&1; then
    echo "📦 Installing psycopg2-binary..."
    pip3 install psycopg2-binary
fi

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "📁 Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Run the Python script
echo "🚀 Loading sample data..."
python3 load_sample_data.py

# Check if Flask app is running
echo ""
echo "🔍 Checking if Flask API is running..."
if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
    echo "✅ Flask API is running!"
    echo "🌐 You can view products at: http://localhost:5000/api/products"
else
    echo "⚠️  Flask API is not running."
    echo "   To start the API server, run: python3 app.py"
fi

# Check if React app is running
echo ""
echo "🔍 Checking if React app is running..."
if curl -s http://localhost:3000 >/dev/null 2>&1; then
    echo "✅ React app is running!"
    echo "🎉 You can view the dashboard at: http://localhost:3000"
else
    echo "⚠️  React app is not running."
    echo "   To start the React app:"
    echo "   1. cd frontend"
    echo "   2. npm start"
fi

echo ""
echo "🎉 Setup complete! Your inventory system now has sample data."
echo "=================================================="