#!/usr/bin/env python3
"""
Script to load sample products via the Flask API
Usage: python3 load_via_api.py
"""

import json
import requests
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000"
SAMPLE_FILE = "sample_products.json"

def load_sample_products_via_api():
    """Load sample products using the Flask API"""
    
    print("🚀 Loading sample products via API...")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding properly")
            return
        print("✅ API is running")
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to API. Make sure it's running on http://localhost:5000")
        return
    
    # Load JSON data
    try:
        with open(SAMPLE_FILE, 'r') as file:
            data = json.load(file)
        products = data['products']
        print(f"📦 Found {len(products)} products to load")
    except FileNotFoundError:
        print(f"❌ Error: {SAMPLE_FILE} file not found!")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error reading JSON file: {e}")
        return
    
    # Check existing products
    try:
        response = requests.get(f"{API_BASE_URL}/api/products")
        if response.status_code == 200:
            existing_products = response.json().get('products', [])
            existing_count = len(existing_products)
            print(f"📊 Found {existing_count} existing products")
            
            if existing_count > 0:
                choice = input(f"⚠️  Database already contains {existing_count} products. Do you want to:\n"
                             "1. Add new products (keeping existing ones)\n"
                             "2. Clear database and load fresh data\n"
                             "3. Cancel operation\n"
                             "Enter choice (1/2/3): ").strip()
                
                if choice == '2':
                    print("🗑️  Clearing existing products...")
                    for product in existing_products:
                        try:
                            requests.delete(f"{API_BASE_URL}/api/products/{product['id']}")
                        except:
                            pass
                    print("✅ Database cleared")
                elif choice == '3':
                    print("❌ Operation cancelled")
                    return
                elif choice != '1':
                    print("❌ Invalid choice. Operation cancelled")
                    return
        else:
            print("⚠️  Could not check existing products")
    except Exception as e:
        print(f"⚠️  Could not check existing products: {e}")
    
    # Load products
    loaded_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, product in enumerate(products, 1):
        try:
            # Prepare product data (remove category if not supported by API)
            product_data = {
                'name': product['name'],
                'sku': product['sku'],
                'description': product['description'],
                'price': product['price'],
                'stock_level': product['stock_level'],
                'min_stock_threshold': product['min_stock_threshold']
            }
            
            # Add category if the API supports it
            if 'category' in product:
                product_data['category'] = product['category']
            
            # Create product via API
            response = requests.post(
                f"{API_BASE_URL}/api/products",
                json=product_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                loaded_count += 1
                print(f"✅ [{i}/{len(products)}] Added: {product['name']} (SKU: {product['sku']})")
            elif response.status_code == 400:
                error_msg = response.json().get('error', 'Unknown error')
                if 'already exists' in error_msg.lower():
                    skipped_count += 1
                    print(f"⏭️  [{i}/{len(products)}] Skipped: {product['name']} (SKU: {product['sku']}) - already exists")
                else:
                    error_count += 1
                    print(f"❌ [{i}/{len(products)}] Error: {product['name']} - {error_msg}")
            else:
                error_count += 1
                print(f"❌ [{i}/{len(products)}] Error: {product['name']} - Status {response.status_code}")
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
            
        except Exception as e:
            error_count += 1
            print(f"❌ [{i}/{len(products)}] Error: {product['name']} - {str(e)}")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"✅ Products loaded successfully: {loaded_count}")
    print(f"⏭️  Products skipped (duplicates): {skipped_count}")
    print(f"❌ Products with errors: {error_count}")
    
    # Show final status
    try:
        response = requests.get(f"{API_BASE_URL}/api/products/analytics")
        if response.status_code == 200:
            analytics = response.json().get('analytics', {})
            print(f"\n📈 FINAL STATUS:")
            print(f"   📦 Total products: {analytics.get('total_products', 'N/A')}")
            print(f"   🟡 Low stock: {analytics.get('low_stock_count', 'N/A')}")
            print(f"   🔴 Out of stock: {analytics.get('out_of_stock_count', 'N/A')}")
    except:
        pass
    
    print(f"\n🎉 Sample data loading completed!")
    print(f"🌐 View products at: http://localhost:3000")
    print(f"🔗 API endpoint: http://localhost:5000/api/products")

if __name__ == "__main__":
    print("🚀 Inventory Management - API Sample Data Loader")
    print("=" * 50)
    load_sample_products_via_api() 