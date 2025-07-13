# 🧪 Testing Guide - Smart Retail App

> **Note**: For complete project information, deployment, and API reference, see **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)**

## 🚀 Quick Start Commands

### **Start the Application**
```bash
# 1. Start port forwarding for backend and monitoring
kubectl port-forward service/flask-service 5000:5000 &
kubectl port-forward service/grafana-service 3001:3000 &
kubectl port-forward service/prometheus-service 9090:9090 &

# 2. Start the React frontend (in a new terminal)
cd frontend
npm start
```

### **Access URLs**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Prometheus**: http://localhost:9090

### **Stop Port Forwarding**
```bash
# Kill all port forwarding processes
pkill -f "kubectl port-forward"
```

---

## 📋 Manual Testing Checklist

### 1. **Backend API Testing**
- [ ] **Health Check**: Visit [http://localhost:5000/api/health](http://localhost:5000/api/health)
  - Should return: `{"status": "healthy", "message": "Inventory API is running"}`

- [ ] **Product Endpoints** (Use Postman, Insomnia, or curl):
  - [ ] `GET /api/products` — Should return product list (can be empty)
  - [ ] `POST /api/products` — Add a product:
    ```json
    {
      "name": "Test Product",
      "sku": "TEST123",
      "description": "A test product for verification",
      "stock_level": 10,
      "min_stock_threshold": 2,
      "price": 19.99
    }
    ```
  - [ ] `GET /api/products/<id>` — Get specific product details
  - [ ] `PUT /api/products/<id>` — Update product:
    ```json
    {
      "stock_level": 15,
      "price": 24.99
    }
    ```
  - [ ] `POST /api/products/<id>/restock` — Restock product:
    ```json
    {
      "quantity": 5,
      "notes": "Test restock"
    }
    ```
  - [ ] `DELETE /api/products/<id>` — Delete product
  - [ ] `GET /api/products/analytics` — Should return analytics data
  - [ ] `GET /api/products/low-stock` — Should return low stock products
  - [ ] `GET /api/restocks` — Should return restock history

### 2. **Frontend Testing**
- [ ] **Dashboard**: Go to [http://localhost:3000](http://localhost:3000)
  - [ ] Dashboard loads without errors
  - [ ] Product list displays (can be empty initially)
  - [ ] Navigation works between sections

- [ ] **Product Management**:
  - [ ] Add a new product via the UI
  - [ ] Edit an existing product
  - [ ] Restock a product
  - [ ] Delete a product
  - [ ] View product details

- [ ] **Analytics**:
  - [ ] View stock analytics
  - [ ] See low stock alerts
  - [ ] Check restock history

### 3. **Monitoring & Observability**
- [ ] **Prometheus**: Visit [http://localhost:9090](http://localhost:9090)
  - [ ] Check "Targets" page — Flask API should show "UP"
  - [ ] Search for metrics:
    - `http_requests_total`
    - `http_request_duration_seconds`
    - `product_stock_level`
    - `low_stock_alerts_total`
    - `restock_operations_total`

- [ ] **Grafana**: Visit [http://localhost:3001](http://localhost:3001)
  - [ ] Login with admin/admin123
  - [ ] Open "Inventory Management Dashboard"
  - [ ] Verify panels show:
    - API request rate
    - Response latency
    - Stock levels
    - Business metrics

### 4. **Security & Validation Testing**
- [ ] **Input Validation**:
  - [ ] Try to create product with invalid SKU (too short)
  - [ ] Try to create product with negative price
  - [ ] Try to restock with negative quantity
  - [ ] All should return 400 Bad Request

- [ ] **Rate Limiting**:
  - [ ] Make 15+ requests quickly to `/api/products` (POST)
  - [ ] Should get 429 Too Many Requests after limit

- [ ] **Security Headers**:
  - [ ] Check response headers include:
    - `X-Content-Type-Options: nosniff`
    - `X-Frame-Options: DENY`
    - `X-XSS-Protection: 1; mode=block`

### 5. **Database & Persistence**
- [ ] **Data Persistence**:
  - [ ] Add a product
  - [ ] Restart the Flask deployment
  - [ ] Verify product still exists
  - [ ] Check data in PostgreSQL directly:
    ```bash
    kubectl exec -it postgres-deployment-<pod-id> -- psql -U inventory_user -d inventory_db -c "SELECT * FROM products;"
    ```

### 6. **Logs & Debugging**
- [ ] **Backend Logs**:
  ```bash
  kubectl logs -f deployment/flask-deployment
  ```
  - [ ] Look for errors or warnings
  - [ ] Verify logging messages for operations

- [ ] **Frontend Console**:
  - [ ] Open browser developer tools
  - [ ] Check console for JavaScript errors
  - [ ] Verify network requests succeed

### 7. **Automated Health Check**
- [ ] **Run Health Check Script**:
  ```bash
  python3 health_check.py
  ```
  - [ ] All 5 checks should pass:
    - ✅ API Health Check
    - ✅ Database Connection
    - ✅ Metrics Endpoint
    - ✅ Rate Limiting
    - ✅ Input Validation

---

## 🤖 Automated Testing Scripts

### Quick API Check Script
Create `quick_api_check.py`:
```python
#!/usr/bin/env python3
"""
Quick API endpoint verification script
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(method, path, data=None, expected_status=200):
    """Test an API endpoint"""
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{BASE_URL}{path}")
        elif method.upper() == 'POST':
            response = requests.post(f"{BASE_URL}{path}", json=data)
        elif method.upper() == 'PUT':
            response = requests.put(f"{BASE_URL}{path}", json=data)
        elif method.upper() == 'DELETE':
            response = requests.delete(f"{BASE_URL}{path}")
        
        status = "✅" if response.status_code == expected_status else "❌"
        print(f"{status} {method} {path}: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                result = response.json()
                if 'success' in result:
                    print(f"   Success: {result['success']}")
            except:
                pass
        
        return response.status_code == expected_status
    except Exception as e:
        print(f"❌ {method} {path}: Error - {e}")
        return False

def main():
    print("🚀 Quick API Test Suite")
    print("=" * 40)
    
    tests = [
        ('GET', '/api/health'),
        ('GET', '/api/products'),
        ('GET', '/api/products/analytics'),
        ('GET', '/api/products/low-stock'),
        ('GET', '/api/restocks'),
        ('GET', '/metrics'),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, path in tests:
        if test_endpoint(method, path):
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Results: {passed}/{total} endpoints working")
    
    if passed == total:
        print("🎉 All API endpoints are working!")
    else:
        print("⚠️  Some endpoints failed!")

if __name__ == "__main__":
    main()
```

### End-to-End Test Script
Create `e2e_test.py`:
```python
#!/usr/bin/env python3
"""
End-to-End test script for the Smart Retail App
"""

import requests
import time
import json

BASE_URL = "http://localhost:5000"

def create_test_product():
    """Create a test product and return its ID"""
    product_data = {
        "name": f"E2E Test Product {int(time.time())}",
        "sku": f"E2E-{int(time.time())}",
        "description": "Product created by E2E test",
        "stock_level": 10,
        "min_stock_threshold": 5,
        "price": 29.99
    }
    
    response = requests.post(f"{BASE_URL}/api/products", json=product_data)
    if response.status_code == 201:
        product_id = response.json()['product']['id']
        print(f"✅ Created test product with ID: {product_id}")
        return product_id
    else:
        print(f"❌ Failed to create test product: {response.status_code}")
        return None

def test_product_lifecycle():
    """Test complete product lifecycle"""
    print("🔄 Testing Product Lifecycle...")
    
    # 1. Create product
    product_id = create_test_product()
    if not product_id:
        return False
    
    # 2. Get product
    response = requests.get(f"{BASE_URL}/api/products/{product_id}")
    if response.status_code != 200:
        print(f"❌ Failed to get product: {response.status_code}")
        return False
    print("✅ Retrieved product")
    
    # 3. Update product
    update_data = {"stock_level": 15, "price": 34.99}
    response = requests.put(f"{BASE_URL}/api/products/{product_id}", json=update_data)
    if response.status_code != 200:
        print(f"❌ Failed to update product: {response.status_code}")
        return False
    print("✅ Updated product")
    
    # 4. Restock product
    restock_data = {"quantity": 5, "notes": "E2E test restock"}
    response = requests.post(f"{BASE_URL}/api/products/{product_id}/restock", json=restock_data)
    if response.status_code != 200:
        print(f"❌ Failed to restock product: {response.status_code}")
        return False
    print("✅ Restocked product")
    
    # 5. Delete product
    response = requests.delete(f"{BASE_URL}/api/products/{product_id}")
    if response.status_code != 200:
        print(f"❌ Failed to delete product: {response.status_code}")
        return False
    print("✅ Deleted product")
    
    return True

def test_analytics():
    """Test analytics endpoints"""
    print("📊 Testing Analytics...")
    
    endpoints = [
        '/api/products/analytics',
        '/api/products/low-stock',
        '/api/restocks'
    ]
    
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"✅ {endpoint} working")
        else:
            print(f"❌ {endpoint} failed: {response.status_code}")

def main():
    print("🧪 End-to-End Test Suite")
    print("=" * 50)
    
    # Test product lifecycle
    if test_product_lifecycle():
        print("✅ Product lifecycle test passed")
    else:
        print("❌ Product lifecycle test failed")
    
    print()
    
    # Test analytics
    test_analytics()
    
    print()
    print("=" * 50)
    print("🎉 E2E testing completed!")

if __name__ == "__main__":
    main()
```

---

## 🚀 Running the Tests

### 1. **Quick API Check**
```bash
python3 quick_api_check.py
```

### 2. **End-to-End Test**
```bash
python3 e2e_test.py
```

### 3. **Health Check**
```bash
python3 health_check.py
```

### 4. **Load Testing**
```bash
python3 test_monitoring.py
```

---

## 📊 Expected Results

### ✅ **All Tests Should Pass**
- API endpoints return correct status codes
- Data persists across operations
- Monitoring metrics are collected
- Security features work (validation, rate limiting)
- Frontend displays data correctly
- Grafana dashboards show metrics

### ❌ **Common Issues to Check**
- **Port forwarding not set up**: Ensure kubectl port-forward is running
- **Database connection issues**: Check PostgreSQL pod status
- **Frontend not loading**: Verify React app is running on port 3000
- **Metrics not showing**: Check Prometheus targets and Grafana datasource

---

## 🔧 Troubleshooting

### If Tests Fail:
1. **Check pod status**: `kubectl get pods`
2. **View logs**: `kubectl logs deployment/flask-deployment`
3. **Verify port forwarding**: `kubectl port-forward service/flask-service 5000:5000`
4. **Check health**: `python3 health_check.py`

### If Frontend Issues:
1. **Check React app**: Ensure it's running on localhost:3000
2. **Browser console**: Look for JavaScript errors
3. **Network tab**: Check API requests

### If Monitoring Issues:
1. **Prometheus targets**: Check if Flask API is UP
2. **Grafana login**: Verify admin/admin123 credentials
3. **Dashboard**: Ensure Prometheus datasource is configured

---

## ✅ Success Criteria

Your app is **fully working** when:
- [ ] All manual checklist items pass
- [ ] All automated tests pass
- [ ] Frontend displays data correctly
- [ ] Monitoring shows real-time metrics
- [ ] No errors in logs
- [ ] Security features are active

**Congratulations!** 🎉 Your Smart Retail App is production-ready! 