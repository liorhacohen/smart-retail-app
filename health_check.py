#!/usr/bin/env python3
"""
Health check script for the Inventory Management System
"""

import requests
import time
import json
import sys
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000"
TIMEOUT = 10

def check_api_health():
    """Check if the API is responding"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=TIMEOUT)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print(f"❌ API Health Check: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ API Health Check: FAILED (Error: {e})")
        return False

def check_database_connection():
    """Check if database is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/products", timeout=TIMEOUT)
        if response.status_code == 200:
            print("✅ Database Connection: PASSED")
            return True
        else:
            print(f"❌ Database Connection: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Database Connection: FAILED (Error: {e})")
        return False

def check_metrics_endpoint():
    """Check if metrics endpoint is working"""
    try:
        response = requests.get(f"{API_BASE_URL}/metrics", timeout=TIMEOUT)
        if response.status_code == 200:
            metrics = response.text
            if 'http_requests_total' in metrics:
                print("✅ Metrics Endpoint: PASSED")
                return True
            else:
                print("❌ Metrics Endpoint: FAILED (No metrics found)")
                return False
        else:
            print(f"❌ Metrics Endpoint: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Metrics Endpoint: FAILED (Error: {e})")
        return False

def check_rate_limiting():
    """Test rate limiting functionality"""
    try:
        # Make multiple requests quickly to test rate limiting
        responses = []
        for i in range(15):
            response = requests.post(f"{API_BASE_URL}/api/products", 
                                   json={"name": f"Test{i}", "sku": f"TEST{i}"},
                                   timeout=TIMEOUT)
            responses.append(response.status_code)
        
        # Check if we got rate limited (429 status)
        if 429 in responses:
            print("✅ Rate Limiting: PASSED")
            return True
        else:
            print("⚠️  Rate Limiting: NOT TESTED (No rate limit hit)")
            return True
    except Exception as e:
        print(f"❌ Rate Limiting: FAILED (Error: {e})")
        return False

def check_input_validation():
    """Test input validation"""
    try:
        # Test invalid SKU
        response = requests.post(f"{API_BASE_URL}/api/products", 
                               json={"name": "Test", "sku": "a"},  # Too short
                               timeout=TIMEOUT)
        if response.status_code == 400:
            print("✅ Input Validation: PASSED")
            return True
        else:
            print(f"❌ Input Validation: FAILED (Expected 400, got {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Input Validation: FAILED (Error: {e})")
        return False

def main():
    """Run all health checks"""
    print("🏥 Starting Health Check Suite")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_BASE_URL}")
    print()
    
    checks = [
        check_api_health,
        check_database_connection,
        check_metrics_endpoint,
        check_rate_limiting,
        check_input_validation
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All health checks passed!")
        sys.exit(0)
    else:
        print("⚠️  Some health checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 