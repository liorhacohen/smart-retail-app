# This is a test to add a product to the application (app.py)
import requests

url = "http://127.0.0.1:5000/api/products"
data = {
    "name": "חלב",
    "sku": "milk-001",
    "stock": 10
}
response = requests.post(url, json=data)
print(response.json())