"""
Unit tests for Smart Retail App Flask backend
"""
import json
import os
import sys


import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import Product, app, db


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "name": "Test Product",
        "sku": "TEST-001",
        "description": "A test product for unit testing",
        "stock_level": 50,
        "min_stock_threshold": 10,
        "price": 29.99,
    }


@pytest.fixture
def sample_product(client, sample_product_data):
    """Create a sample product in the database"""
    with app.app_context():
        product = Product(**sample_product_data)
        db.session.add(product)
        db.session.commit()
        return product


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test that health check returns 200"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"


class TestProducts:
    """Test product-related endpoints"""

    def test_get_all_products_empty(self, client):
        """Test getting all products when database is empty"""
        response = client.get("/api/products")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["products"] == []
        assert data["total"] == 0

    def test_get_all_products_with_data(self, client, sample_product):
        """Test getting all products when database has data"""
        response = client.get("/api/products")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["products"]) == 1
        assert data["total"] == 1
        assert data["products"][0]["name"] == sample_product.name

    def test_get_specific_product(self, client, sample_product):
        """Test getting a specific product"""
        response = client.get(f"/api/products/{sample_product.id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["product"]["id"] == sample_product.id
        assert data["product"]["name"] == sample_product.name

    def test_get_nonexistent_product(self, client):
        """Test getting a product that doesn't exist"""
        response = client.get("/api/products/999")
        assert response.status_code == 404

    def test_create_product_valid(self, client, sample_product_data):
        """Test creating a product with valid data"""
        response = client.post(
            "/api/products",
            data=json.dumps(sample_product_data),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["product"]["name"] == sample_product_data["name"]
        assert data["product"]["sku"] == sample_product_data["sku"]

    def test_create_product_invalid_data(self, client):
        """Test creating a product with invalid data"""
        invalid_data = {
            "name": "",  # Empty name
            "sku": "INVALID SKU",  # Invalid SKU format
            "price": -10,  # Negative price
        }
        response = client.post(
            "/api/products",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_create_product_duplicate_sku(self, client, sample_product):
        """Test creating a product with duplicate SKU"""
        duplicate_data = {
            "name": "Another Product",
            "sku": sample_product.sku,  # Same SKU
            "description": "Another product",
            "stock_level": 25,
            "price": 19.99,
        }
        response = client.post(
            "/api/products",
            data=json.dumps(duplicate_data),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_update_product_valid(self, client, sample_product):
        """Test updating a product with valid data"""
        update_data = {"name": "Updated Product Name", "stock_level": 75}
        response = client.put(
            f"/api/products/{sample_product.id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["product"]["name"] == update_data["name"]
        assert data["product"]["stock_level"] == update_data["stock_level"]

    def test_update_nonexistent_product(self, client):
        """Test updating a product that doesn't exist"""
        update_data = {"name": "Updated Name"}
        response = client.put(
            "/api/products/999",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_delete_product(self, client, sample_product):
        """Test deleting a product"""
        response = client.delete(f"/api/products/{sample_product.id}")
        assert response.status_code == 200

        # Verify product is deleted
        get_response = client.get(f"/api/products/{sample_product.id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_product(self, client):
        """Test deleting a product that doesn't exist"""
        response = client.delete("/api/products/999")
        assert response.status_code == 404


class TestRestocking:
    """Test restocking-related endpoints"""

    def test_restock_product_valid(self, client, sample_product):
        """Test restocking a product with valid data"""
        restock_data = {"quantity": 25, "notes": "Test restock operation"}
        original_stock = sample_product.stock_level

        response = client.post(
            f"/api/products/{sample_product.id}/restock",
            data=json.dumps(restock_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["restock"]["quantity_added"] == restock_data["quantity"]
        assert data["restock"]["new_stock"] == original_stock + restock_data["quantity"]

    def test_restock_nonexistent_product(self, client):
        """Test restocking a product that doesn't exist"""
        restock_data = {"quantity": 25}
        response = client.post(
            "/api/products/999/restock",
            data=json.dumps(restock_data),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_restock_invalid_quantity(self, client, sample_product):
        """Test restocking with invalid quantity"""
        restock_data = {"quantity": -5}  # Negative quantity
        response = client.post(
            f"/api/products/{sample_product.id}/restock",
            data=json.dumps(restock_data),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_get_restock_history(self, client, sample_product):
        """Test getting restock history"""
        # First, create a restock operation
        restock_data = {"quantity": 10}
        client.post(
            f"/api/products/{sample_product.id}/restock",
            data=json.dumps(restock_data),
            content_type="application/json",
        )

        # Then get the history
        response = client.get("/api/restocks")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["restocks"]) >= 1


class TestAnalytics:
    """Test analytics endpoints"""

    def test_get_low_stock_products(self, client, sample_product):
        """Test getting low stock products"""
        # Update product to have low stock
        with app.app_context():
            sample_product.stock_level = 5  # Below threshold
            db.session.commit()

        response = client.get("/api/products/low-stock")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data["products"]) >= 1
        assert data["products"][0]["is_low_stock"] == True

    def test_get_stock_analytics(self, client, sample_product):
        """Test getting stock analytics"""
        response = client.get("/api/products/analytics")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "total_products" in data
        assert "total_stock_value" in data
        assert "low_stock_count" in data


class TestMetrics:
    """Test Prometheus metrics endpoint"""

    def test_metrics_endpoint(self, client):
        """Test that metrics endpoint returns data"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "http_requests_total" in response.data.decode()


class TestErrorHandling:
    """Test error handling"""

    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_invalid_json(self, client):
        """Test handling of invalid JSON"""
        response = client.post(
            "/api/products", data="invalid json", content_type="application/json"
        )
        assert response.status_code == 400


class TestValidation:
    """Test input validation functions"""

    def test_sku_validation(self):
        """Test SKU validation"""
        from app import validate_sku

        # Valid SKUs
        assert validate_sku("ABC123") == True
        assert validate_sku("PROD-001") == True
        assert validate_sku("test_sku") == True

        # Invalid SKUs
        assert validate_sku("") == False
        assert validate_sku("AB") == False  # Too short
        assert validate_sku("A" * 25) == False  # Too long
        assert validate_sku("INVALID SKU") == False  # Contains space

    def test_price_validation(self):
        """Test price validation"""
        from app import validate_price

        # Valid prices
        assert validate_price(10.99) == True
        assert validate_price(0) == True
        assert validate_price("15.50") == True

        # Invalid prices
        assert validate_price(-10) == False
        assert validate_price("invalid") == False

    def test_stock_level_validation(self):
        """Test stock level validation"""
        from app import validate_stock_level

        # Valid stock levels
        assert validate_stock_level(100) == True
        assert validate_stock_level(0) == True
        assert validate_stock_level("50") == True

        # Invalid stock levels
        assert validate_stock_level(-5) == False
        assert validate_stock_level("invalid") == False


if __name__ == "__main__":
    pytest.main([__file__])
