#!/bin/bash

# Script to update/reload sample data from sample_products.json
# This script provides multiple options for loading sample data

echo "🔄 Sample Data Management"
echo "=========================="

# Check if sample_products.json exists
if [ ! -f "sample_products.json" ]; then
    echo "❌ Error: sample_products.json not found!"
    echo "   Please make sure the JSON file is in the current directory."
    exit 1
fi

echo "📁 Found sample_products.json"
echo ""

# Show menu
echo "Choose an option:"
echo "1. Load via API (recommended for running app)"
echo "2. Load via direct database access"
echo "3. View current sample data structure"
echo "4. Check current database status"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Loading sample data via API..."
        echo "   Make sure your Flask API is running on http://localhost:5000"
        echo ""
        
        # Check if API is running
        if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
            echo "✅ API is running, proceeding..."
            python3 load_via_api.py
        else
            echo "❌ API is not running!"
            echo "   Please start the API first:"
            echo "   kubectl port-forward service/flask-service 5000:5000 &"
            echo "   Or run: python3 app.py"
        fi
        ;;
    2)
        echo ""
        echo "🗄️  Loading sample data via direct database access..."
        echo "   Make sure PostgreSQL is running and accessible"
        echo ""
        
        # Check if Python script exists
        if [ ! -f "load_sample_data.py" ]; then
            echo "❌ Error: load_sample_data.py not found!"
            exit 1
        fi
        
        # Run the Python script
        python3 load_sample_data.py
        ;;
    3)
        echo ""
        echo "📋 Sample data structure:"
        echo "=========================="
        
        # Show first few products
        python3 -c "
import json
try:
    with open('sample_products.json', 'r') as f:
        data = json.load(f)
    products = data['products']
    print(f'Total products: {len(products)}')
    print('')
    print('Sample products:')
    for i, product in enumerate(products[:3], 1):
        print(f'{i}. {product[\"name\"]} (SKU: {product[\"sku\"]})')
        print(f'   Price: ${product[\"price\"]}')
        print(f'   Stock: {product[\"stock_level\"]}')
        print(f'   Category: {product.get(\"category\", \"N/A\")}')
        print('')
    if len(products) > 3:
        print(f'... and {len(products) - 3} more products')
except Exception as e:
    print(f'Error reading file: {e}')
"
        ;;
    4)
        echo ""
        echo "📊 Current database status:"
        echo "==========================="
        
        # Try to get status via API
        if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
            echo "✅ API is running"
            
            # Get products count
            products_response=$(curl -s http://localhost:5000/api/products)
            if [ $? -eq 0 ]; then
                product_count=$(echo "$products_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(len(data.get('products', [])))
except:
    print('0')
")
                echo "📦 Products in database: $product_count"
            fi
            
            # Get analytics
            analytics_response=$(curl -s http://localhost:5000/api/products/analytics)
            if [ $? -eq 0 ]; then
                echo "$analytics_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    analytics = data.get('analytics', {})
    print(f'📈 Total products: {analytics.get(\"total_products\", \"N/A\")}')
    print(f'🟡 Low stock: {analytics.get(\"low_stock_count\", \"N/A\")}')
    print(f'🔴 Out of stock: {analytics.get(\"out_of_stock_count\", \"N/A\")}')
except:
    print('Could not parse analytics')
"
            fi
        else
            echo "❌ API is not running"
            echo "   Start it with: kubectl port-forward service/flask-service 5000:5000 &"
        fi
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please enter 1-5."
        exit 1
        ;;
esac

echo ""
echo "🎉 Operation completed!" 