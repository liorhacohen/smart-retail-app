#!/usr/bin/env python3
"""
Simple API test script for Inventory Management System
Run this script to test all API endpoints after starting the application
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000/api"
headers = {"Content-Type": "application/json"}

def print_response(response, description):
    """Print formatted response for testing"""
    print(f"\n{'='*50}")
    print(f"TEST: {description}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Text: {response.text}")

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    return response.status_code == 200

def test_get_all_products():
    """Test getting all products"""
    response = requests.get(f"{BASE_URL}/products")
    print_response(response, "Get All Products")
    return response.status_code == 200

def test_create_product():
    """Test creating a new product"""
    product_data = {
        "name": "Test Gaming Keyboard",
        "sku": "TGK001",
        "description": "RGB mechanical gaming keyboard for testing",
        "stock_level": 25,
        "min_stock_threshold": 5,
        "price": 129.99
    }
    
    response = requests.post(f"{BASE_URL}/products", 
                           headers=headers, 
                           json=product_data)
    print_response(response, "Create New Product")
    
    if response.status_code == 201:
        return response.json().get('product', {}).get('id')
    return None

def test_get_specific_product(product_id):
    """Test getting specific product details"""
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    print_response(response, f"Get Product ID: {product_id}")
    return response.status_code == 200

def test_update_product(product_id):
    """Test updating product information"""
    update_data = {
        "stock_level": 30,
        "description": "Updated: RGB mechanical gaming keyboard with macro keys"
    }
    
    response = requests.put(f"{BASE_URL}/products/{product_id}",
                          headers=headers,
                          json=update_data)
    print_response(response, f"Update Product ID: {product_id}")
    return response.status_code == 200

def test_restock_product(product_id):
    """Test restocking a product"""
    restock_data = {
        "quantity": 15,
        "notes": "Test restock operation"
    }
    
    response = requests.post(f"{BASE_URL}/products/{product_id}/restock",
                           headers=headers,
                           json=restock_data)
    print_response(response, f"Restock Product ID: {product_id}")
    return response.status_code == 200

def test_get_restock_history():
    """Test getting restock history"""
    response = requests.get(f"{BASE_URL}/restocks")
    print_response(response, "Get Restock History")
    return response.status_code == 200

def test_get_low_stock_products():
    """Test getting low stock products"""
    response = requests.get(f"{BASE_URL}/products/low-stock")
    print_response(response, "Get Low Stock Products")
    return response.status_code == 200

def test_get_analytics():
    """Test getting stock analytics"""
    response = requests.get(f"{BASE_URL}/products/analytics")
    print_response(response, "Get Stock Analytics")
    return response.status_code == 200

def test_delete_product(product_id):
    """Test deleting a product"""
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    print_response(response, f"Delete Product ID: {product_id}")
    return response.status_code == 200

def run_all_tests():
    """Run comprehensive API tests"""
    print("Starting Inventory Management System API Tests")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Health Check
    print("\n🏥 Testing Health Check...")
    test_results.append(("Health Check", test_health_check()))
    
    # Wait a moment for the system to be ready
    time.sleep(1)
    
    # Test 2: Get All Products (should return sample data)
    print("\n📦 Testing Get All Products...")
    test_results.append(("Get All Products", test_get_all_products()))
    
    # Test 3: Create New Product
    print("\n➕ Testing Create Product...")
    product_id = test_create_product()
    test_results.append(("Create Product", product_id is not None))
    
    if product_id:
        # Test 4: Get Specific Product
        print(f"\n🔍 Testing Get Specific Product (ID: {product_id})...")
        test_results.append(("Get Specific Product", test_get_specific_product(product_id)))
        
        # Test 5: Update Product
        print(f"\n✏️ Testing Update Product (ID: {product_id})...")
        test_results.append(("Update Product", test_update_product(product_id)))
        
        # Test 6: Restock Product
        print(f"\n📈 Testing Restock Product (ID: {product_id})...")
        test_results.append(("Restock Product", test_restock_product(product_id)))
    
    # Test 7: Get Restock History
    print("\n📋 Testing Get Restock History...")
    test_results.append(("Get Restock History", test_get_restock_history()))
    
    # Test 8: Get Low Stock Products
    print("\n⚠️ Testing Get Low Stock Products...")
    test_results.append(("Get Low Stock Products", test_get_low_stock_products()))
    
    # Test 9: Get Analytics
    print("\n📊 Testing Get Analytics...")
    test_results.append(("Get Analytics", test_get_analytics()))
    
    # Test 10: Delete Product (cleanup)
    if product_id:
        print(f"\n🗑️ Testing Delete Product (ID: {product_id})...")
        test_results.append(("Delete Product", test_delete_product(product_id)))
    
    # Print Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed. Check the logs above for details.")

def test_error_cases():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("TESTING ERROR CASES")
    print("=" * 60)
    
    # Test invalid product ID
    print("\n❌ Testing Invalid Product ID...")
    response = requests.get(f"{BASE_URL}/products/99999")
    print_response(response, "Get Non-existent Product")
    
    # Test invalid JSON
    print("\n❌ Testing Invalid JSON...")
    response = requests.post(f"{BASE_URL}/products", 
                           headers=headers, 
                           data="invalid json")
    print_response(response, "Create Product with Invalid JSON")
    
    # Test missing required fields
    print("\n❌ Testing Missing Required Fields...")
    response = requests.post(f"{BASE_URL}/products",
                           headers=headers,
                           json={"description": "Missing name and SKU"})
    print_response(response, "Create Product Missing Required Fields")

if __name__ == "__main__":
    try:
        print("🚀 Starting API tests...")
        print("Make sure the application is running on http://localhost:5000")
        
        # Wait for user confirmation
        input("\nPress Enter to continue with the tests...")
        
        # Run main tests
        run_all_tests()
        
        # Ask if user wants to test error cases
        test_errors = input("\nDo you want to test error cases? (y/n): ").lower().strip()
        if test_errors == 'y':
            test_error_cases()
        
        print("\n✨ Testing completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API")
        print("Make sure the application is running with: docker-compose up")
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")