#!/usr/bin/env python3
"""
Monitoring Test Script for Inventory Management System
"""

import requests
import json
import time
import random
import threading
from datetime import datetime

BASE_URL = "http://localhost"
PROMETHEUS_URL = "http://localhost/prometheus"
GRAFANA_URL = "http://localhost/grafana"

class MonitoringTester:
    def __init__(self):
        self.session = requests.Session()
        self.products_created = []
        
    def test_endpoints_health(self):
        """Test if all monitoring endpoints are accessible"""
        print("🔍 Testing endpoint accessibility...")
        
        endpoints = {
            "Main API": f"{BASE_URL}/api/health",
            "Metrics": f"{BASE_URL}/metrics", 
            "Prometheus": f"{PROMETHEUS_URL}/api/v1/targets",
            "Grafana": f"{GRAFANA_URL}/api/health"
        }
        
        results = {}
        for name, url in endpoints.items():
            try:
                response = self.session.get(url, timeout=5)
                status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                results[name] = status
                print(f"  {name:15} {status}")
            except Exception as e:
                results[name] = f"❌ ERROR: {str(e)}"
                print(f"  {name:15} ❌ ERROR: {str(e)}")
        
        return results
    
    def generate_api_traffic(self, duration_minutes=3):
        """Generate realistic API traffic to populate metrics"""
        print(f"🚦 Generating API traffic for {duration_minutes} minutes...")
        
        end_time = time.time() + (duration_minutes * 60)
        request_count = 0
        
        while time.time() < end_time:
            try:
                action = random.choices(
                    ['get_products', 'get_product', 'create_product', 'restock', 'analytics'],
                    weights=[40, 20, 10, 15, 15]
                )[0]
                
                if action == 'get_products':
                    response = self.session.get(f"{BASE_URL}/api/products")
                    
                elif action == 'create_product':
                    product_data = {
                        "name": f"Monitor Test Product {random.randint(1000, 9999)}",
                        "sku": f"MON{random.randint(1000, 9999)}",
                        "description": "Auto-generated monitoring test product",
                        "stock_level": random.randint(0, 100),
                        "min_stock_threshold": random.randint(5, 20),
                        "price": round(random.uniform(10, 500), 2)
                    }
                    response = self.session.post(
                        f"{BASE_URL}/api/products",
                        json=product_data,
                        headers={"Content-Type": "application/json"}
                    )
                    if response.status_code == 201:
                        product_id = response.json().get('product', {}).get('id')
                        if product_id:
                            self.products_created.append(product_id)
                            
                elif action == 'analytics':
                    endpoints = ['/api/products/analytics', '/api/products/low-stock']
                    endpoint = random.choice(endpoints)
                    response = self.session.get(f"{BASE_URL}{endpoint}")
                
                request_count += 1
                time.sleep(random.uniform(0.1, 2.0))
                
            except Exception as e:
                print(f"⚠️ Error during traffic generation: {e}")
                
        print(f"✅ Generated {request_count} API requests")
        return request_count
    
    def validate_prometheus_metrics(self):
        """Validate that Prometheus is collecting metrics"""
        print("📊 Validating Prometheus metrics collection...")
        
        metrics_to_check = [
            'flask_request_total',
            'flask_request_duration_seconds',
            'inventory_total_products',
            'inventory_total_value'
        ]
        
        results = {}
        for metric in metrics_to_check:
            try:
                response = self.session.get(
                    f"{PROMETHEUS_URL}/api/v1/query",
                    params={'query': metric},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success' and data.get('data', {}).get('result'):
                        value = data['data']['result'][0]['value'][1]
                        results[metric] = f"✅ {value}"
                        print(f"  {metric:35} ✅ {value}")
                    else:
                        results[metric] = "❌ No data"
                        print(f"  {metric:35} ❌ No data")
                else:
                    results[metric] = f"❌ HTTP {response.status_code}"
                    print(f"  {metric:35} ❌ HTTP {response.status_code}")
                    
            except Exception as e:
                results[metric] = f"❌ ERROR: {str(e)}"
                print(f"  {metric:35} ❌ ERROR: {str(e)}")
        
        return results

def run_monitoring_test():
    """Run comprehensive monitoring validation"""
    print("🚀 Starting Monitoring Test")
    print("=" * 50)
    
    tester = MonitoringTester()
    
    # Test endpoints
    print("\n1️⃣ ENDPOINT ACCESSIBILITY TEST")
    print("-" * 40)
    endpoint_results = tester.test_endpoints_health()
    
    # Generate traffic
    print("\n2️⃣ API TRAFFIC GENERATION")
    print("-" * 40)
    traffic_count = tester.generate_api_traffic(duration_minutes=2)
    
    # Wait for metrics
    print("\n⏳ Waiting 30 seconds for metrics collection...")
    time.sleep(30)
    
    # Validate metrics
    print("\n3️⃣ PROMETHEUS METRICS VALIDATION")
    print("-" * 40)
    metrics_results = tester.validate_prometheus_metrics()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    all_endpoints_ok = all("✅" in status for status in endpoint_results.values())
    metrics_working = sum(1 for result in metrics_results.values() if "✅" in result)
    
    print(f"Endpoints:        {'✅ ALL OK' if all_endpoints_ok else '❌ SOME FAILED'}")
    print(f"Metrics:          ✅ {metrics_working}/{len(metrics_results)} working")
    print(f"Traffic:          ✅ {traffic_count} requests generated")
    
    if all_endpoints_ok and metrics_working >= 2:
        print(f"\n🎉 MONITORING IS WORKING!")
        print("Access Grafana: http://localhost/grafana/ (admin/inventory123)")
        print("Access Prometheus: http://localhost/prometheus/")
    else:
        print(f"\n⚠️ MONITORING NEEDS ATTENTION")
        print("Check deployment and ensure minikube tunnel is running")

if __name__ == "__main__":
    run_monitoring_test()
