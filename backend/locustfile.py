"""
Performance testing with Locust for Smart Retail App
"""
from locust import HttpUser, task, between
import json
import random

class SmartRetailUser(HttpUser):
    """Simulates a user interacting with the Smart Retail App API"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        # Create a test product for this user session
        self.test_product_id = None
        self.create_test_product()
    
    def create_test_product(self):
        """Create a test product for this session"""
        product_data = {
            "name": f"Load Test Product {random.randint(1000, 9999)}",
            "sku": f"LT{random.randint(1000, 9999)}",
            "description": "Product created for load testing",
            "stock_level": random.randint(10, 100),
            "min_stock_threshold": 5,
            "price": round(random.uniform(10.0, 100.0), 2)
        }
        
        response = self.client.post(
            "/api/products",
            json=product_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            self.test_product_id = data.get('product', {}).get('id')
    
    @task(3)
    def get_health_check(self):
        """Health check endpoint - high frequency"""
        self.client.get("/api/health")
    
    @task(5)
    def get_all_products(self):
        """Get all products - high frequency"""
        self.client.get("/api/products")
    
    @task(2)
    def get_specific_product(self):
        """Get specific product - medium frequency"""
        if self.test_product_id:
            self.client.get(f"/api/products/{self.test_product_id}")
    
    @task(1)
    def create_product(self):
        """Create new product - low frequency"""
        product_data = {
            "name": f"Load Test Product {random.randint(10000, 99999)}",
            "sku": f"LT{random.randint(10000, 99999)}",
            "description": "Product created during load test",
            "stock_level": random.randint(10, 100),
            "min_stock_threshold": 5,
            "price": round(random.uniform(10.0, 100.0), 2)
        }
        
        self.client.post(
            "/api/products",
            json=product_data,
            headers={"Content-Type": "application/json"}
        )
    
    @task(2)
    def update_product(self):
        """Update product - medium frequency"""
        if self.test_product_id:
            update_data = {
                "stock_level": random.randint(10, 100),
                "price": round(random.uniform(10.0, 100.0), 2)
            }
            
            self.client.put(
                f"/api/products/{self.test_product_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
    
    @task(1)
    def restock_product(self):
        """Restock product - low frequency"""
        if self.test_product_id:
            restock_data = {
                "quantity": random.randint(5, 25),
                "notes": "Load test restock operation"
            }
            
            self.client.post(
                f"/api/products/{self.test_product_id}/restock",
                json=restock_data,
                headers={"Content-Type": "application/json"}
            )
    
    @task(2)
    def get_restock_history(self):
        """Get restock history - medium frequency"""
        self.client.get("/api/restocks")
    
    @task(3)
    def get_low_stock_products(self):
        """Get low stock products - high frequency"""
        self.client.get("/api/products/low-stock")
    
    @task(2)
    def get_analytics(self):
        """Get analytics - medium frequency"""
        self.client.get("/api/products/analytics")
    
    @task(1)
    def get_metrics(self):
        """Get Prometheus metrics - low frequency"""
        self.client.get("/metrics")
    
    def on_stop(self):
        """Called when a user stops"""
        # Clean up test product
        if self.test_product_id:
            self.client.delete(f"/api/products/{self.test_product_id}")


class AdminUser(HttpUser):
    """Simulates an admin user with different behavior patterns"""
    
    wait_time = between(2, 5)  # Slower, more thoughtful interactions
    
    @task(1)
    def get_health_check(self):
        """Health check"""
        self.client.get("/api/health")
    
    @task(2)
    def get_analytics(self):
        """Get analytics - admin focus"""
        self.client.get("/api/products/analytics")
    
    @task(1)
    def get_restock_history(self):
        """Get restock history - admin focus"""
        self.client.get("/api/restocks")
    
    @task(1)
    def get_low_stock_products(self):
        """Get low stock products - admin focus"""
        self.client.get("/api/products/low-stock")


# Configuration for different load test scenarios
class QuickTest(SmartRetailUser):
    """Quick smoke test - 10 users for 1 minute"""
    pass

class LoadTest(SmartRetailUser):
    """Load test - 50 users for 5 minutes"""
    pass

class StressTest(SmartRetailUser):
    """Stress test - 100 users for 10 minutes"""
    pass

class SpikeTest(SmartRetailUser):
    """Spike test - 200 users for 2 minutes"""
    pass 