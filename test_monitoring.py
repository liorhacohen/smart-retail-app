#!/usr/bin/env python3
"""
Test script to generate load and verify monitoring metrics
"""

import requests
import time
import json
import random
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000"
TEST_DURATION = 60  # seconds
REQUEST_INTERVAL = 2  # seconds

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{API_BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200

def test_metrics_endpoint():
    """Test metrics endpoint"""
    print("📊 Testing metrics endpoint...")
    response = requests.get(f"{API_BASE_URL}/metrics")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        metrics = response.text
        print(f"   Metrics found: {len(metrics.splitlines())} lines")
        # Check for key metrics
        key_metrics = [
            'http_requests_total',
            'http_request_duration_seconds',
            'product_stock_level',
            'low_stock_alerts_total',
            'restock_operations_total'
        ]
        for metric in key_metrics:
            if metric in metrics:
                print(f"   ✅ {metric} found")
            else:
                print(f"   ❌ {metric} not found")
        return True
    return False

def create_test_product():
    """Create a test product"""
    product_data = {
        "name": f"Test Product {datetime.now().strftime('%H%M%S')}",
        "sku": f"TEST-{random.randint(1000, 9999)}",
        "description": "Test product for monitoring",
        "stock_level": random.randint(10, 100),
        "min_stock_threshold": 5,
        "price": round(random.uniform(10.0, 100.0), 2)
    }
    
    response = requests.post(f"{API_BASE_URL}/api/products", json=product_data)
    if response.status_code == 201:
        return response.json()['product']['id']
    return None

def generate_load():
    """Generate load on the API"""
    print(f"🚀 Generating load for {TEST_DURATION} seconds...")
    
    # Create some test products
    product_ids = []
    for i in range(3):
        product_id = create_test_product()
        if product_id:
            product_ids.append(product_id)
            print(f"   Created product {product_id}")
    
    if not product_ids:
        print("   ❌ Failed to create test products")
        return
    
    start_time = time.time()
    request_count = 0
    
    while time.time() - start_time < TEST_DURATION:
        try:
            # Random API operations
            operation = random.choice([
                'get_all_products',
                'get_product',
                'update_product',
                'restock_product'
            ])
            
            if operation == 'get_all_products':
                response = requests.get(f"{API_BASE_URL}/api/products")
            elif operation == 'get_product':
                product_id = random.choice(product_ids)
                response = requests.get(f"{API_BASE_URL}/api/products/{product_id}")
            elif operation == 'update_product':
                product_id = random.choice(product_ids)
                update_data = {
                    "stock_level": random.randint(5, 50),
                    "price": round(random.uniform(10.0, 100.0), 2)
                }
                response = requests.put(f"{API_BASE_URL}/api/products/{product_id}", json=update_data)
            elif operation == 'restock_product':
                product_id = random.choice(product_ids)
                restock_data = {
                    "quantity": random.randint(1, 20),
                    "notes": "Test restock"
                }
                response = requests.post(f"{API_BASE_URL}/api/products/{product_id}/restock", json=restock_data)
            
            request_count += 1
            if response.status_code < 400:
                print(f"   ✅ {operation}: {response.status_code}")
            else:
                print(f"   ❌ {operation}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(REQUEST_INTERVAL)
    
    print(f"   📈 Generated {request_count} requests")

def test_analytics():
    """Test analytics endpoints"""
    print("📈 Testing analytics endpoints...")
    
    # Test low stock products
    response = requests.get(f"{API_BASE_URL}/api/products/low-stock")
    print(f"   Low stock products: {response.status_code}")
    
    # Test stock analytics
    response = requests.get(f"{API_BASE_URL}/api/products/analytics")
    print(f"   Stock analytics: {response.status_code}")
    if response.status_code == 200:
        analytics = response.json()
        print(f"   Total products: {analytics['analytics']['total_products']}")
        print(f"   Low stock count: {analytics['analytics']['low_stock_count']}")

def main():
    """Main test function"""
    print("🧪 Starting Monitoring Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    if not test_health_check():
        print("❌ Health check failed. Is the API running?")
        return
    
    if not test_metrics_endpoint():
        print("❌ Metrics endpoint failed. Check Prometheus configuration.")
        return
    
    # Generate load
    generate_load()
    
    # Test analytics
    test_analytics()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("\n📊 Next steps:")
    print("1. Check Prometheus targets: http://localhost:9090/targets")
    print("2. View metrics: http://localhost:9090/graph")
    print("3. Access Grafana: http://localhost:3000 (admin/admin123)")
    print("4. Check the 'Inventory Management Dashboard'")

if __name__ == "__main__":
    main() 