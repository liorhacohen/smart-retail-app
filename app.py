# Flask Backend for Inventory Management System
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import os
import logging
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import func
import re

# Prometheus monitoring imports
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Input validation functions
def validate_sku(sku):
    """Validate SKU format (alphanumeric, 3-20 characters)"""
    if not sku or not isinstance(sku, str):
        return False
    return bool(re.match(r'^[A-Za-z0-9\-_]{3,20}$', sku))

def validate_price(price):
    """Validate price (positive number)"""
    try:
        price_float = float(price)
        return price_float >= 0
    except (ValueError, TypeError):
        return False

def validate_stock_level(stock_level):
    """Validate stock level (non-negative integer)"""
    try:
        stock_int = int(stock_level)
        return stock_int >= 0
    except (ValueError, TypeError):
        return False

# Prometheus metrics setup
# Request counters
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

# Business metrics
STOCK_LEVEL_GAUGE = Gauge('product_stock_level', 'Current stock level for products', ['product_id', 'product_name', 'sku'])
LOW_STOCK_ALERTS = Counter('low_stock_alerts_total', 'Total low stock alerts', ['product_id', 'product_name'])
RESTOCK_OPERATIONS = Counter('restock_operations_total', 'Total restock operations', ['product_id', 'product_name'])
PRODUCT_OPERATIONS = Counter('product_operations_total', 'Total product operations', ['operation_type'])

# Database configuration
# Build DATABASE_URL from individual environment variables
db_user = os.getenv('DB_USER', 'inventory_user')
db_password = os.getenv('DB_PASSWORD', 'inventory_pass')
db_host = os.getenv('DB_HOST', 'db')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'inventory_db')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 20
}

# Initialize database
db = SQLAlchemy(app)

# Global flag to ensure database tables are created only once
_database_initialized = False

# Database Models
class Product(db.Model):
    """Product model to store product information"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    stock_level = db.Column(db.Integer, default=0, index=True)
    min_stock_threshold = db.Column(db.Integer, default=10)  # Low stock alert threshold
    price = db.Column(db.Float, default=0.0, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert product object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'description': self.description,
            'stock_level': self.stock_level,
            'min_stock_threshold': self.min_stock_threshold,
            'price': self.price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_low_stock': self.stock_level <= self.min_stock_threshold
        }

class RestockLog(db.Model):
    """Restocking log model to track restocking history"""
    __tablename__ = 'restock_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_added = db.Column(db.Integer, nullable=False)
    previous_stock = db.Column(db.Integer, nullable=False)
    new_stock = db.Column(db.Integer, nullable=False)
    restocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationship with Product
    product = db.relationship('Product', backref='restock_history')
    
    def to_dict(self):
        """Convert restock log object to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name,
            'product_sku': self.product.sku,
            'quantity_added': self.quantity_added,
            'previous_stock': self.previous_stock,
            'new_stock': self.new_stock,
            'restocked_at': self.restocked_at.isoformat(),
            'notes': self.notes
        }

# Initialize database tables (Flask 3.0 compatible)
@app.before_request
def create_tables():
    """Create database tables if they don't exist"""
    global _database_initialized
    if not _database_initialized:
        db.create_all()
        _database_initialized = True

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Monitoring middleware
@app.before_request
def before_request():
    """Start timer for request latency measurement"""
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """Record metrics after each request"""
    if hasattr(request, 'start_time'):
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.endpoint).observe(latency)
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint, status=response.status_code).inc()
    return response

# Prometheus metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# API Endpoints

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Inventory API is running'})

# Product Management Endpoints

@app.route('/api/products', methods=['GET'])
def get_all_products():
    """Get all products with their stock levels"""
    try:
        products = Product.query.all()
        
        # Update stock level gauges for all products
        for product in products:
            STOCK_LEVEL_GAUGE.labels(
                product_id=str(product.id), 
                product_name=product.name, 
                sku=product.sku
            ).set(product.stock_level)
        
        return jsonify({
            'success': True,
            'products': [product.to_dict() for product in products],
            'total_count': len(products)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get details of a specific product"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'success': True,
            'product': product.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@app.route('/api/products', methods=['POST'])
@limiter.limit("10 per minute")
def create_product():
    """Add a new product to inventory"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('sku'):
            return jsonify({'success': False, 'error': 'Name and SKU are required'}), 400
        
        # Validate SKU format
        if not validate_sku(data['sku']):
            return jsonify({'success': False, 'error': 'Invalid SKU format. Use 3-20 alphanumeric characters, hyphens, or underscores'}), 400
        
        # Validate price if provided
        if 'price' in data and not validate_price(data['price']):
            return jsonify({'success': False, 'error': 'Price must be a positive number'}), 400
        
        # Validate stock level if provided
        if 'stock_level' in data and not validate_stock_level(data['stock_level']):
            return jsonify({'success': False, 'error': 'Stock level must be a non-negative integer'}), 400
        
        # Check if SKU already exists
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({'success': False, 'error': 'Product with this SKU already exists'}), 400
        
        # Create new product
        product = Product(
            name=data['name'].strip()[:255],  # Limit name length
            sku=data['sku'],
            description=data.get('description', '')[:1000],  # Limit description length
            stock_level=int(data.get('stock_level', 0)),
            min_stock_threshold=int(data.get('min_stock_threshold', 10)),
            price=float(data.get('price', 0.0))
        )
        
        db.session.add(product)
        db.session.commit()
        
        logger.info(f"Product created: {product.sku} - {product.name}")
        
        # Update metrics
        PRODUCT_OPERATIONS.labels(operation_type='create').inc()
        STOCK_LEVEL_GAUGE.labels(
            product_id=str(product.id), 
            product_name=product.name, 
            sku=product.sku
        ).set(product.stock_level)
        
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating product: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product details or stock level"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Update product fields with validation
        if 'name' in data:
            product.name = data['name'].strip()[:255]  # Limit name length
        
        if 'description' in data:
            product.description = data['description'][:1000]  # Limit description length
        
        if 'stock_level' in data:
            if not validate_stock_level(data['stock_level']):
                return jsonify({'success': False, 'error': 'Stock level must be a non-negative integer'}), 400
            product.stock_level = int(data['stock_level'])
        
        if 'min_stock_threshold' in data:
            if not validate_stock_level(data['min_stock_threshold']):
                return jsonify({'success': False, 'error': 'Min stock threshold must be a non-negative integer'}), 400
            product.min_stock_threshold = int(data['min_stock_threshold'])
        
        if 'price' in data:
            if not validate_price(data['price']):
                return jsonify({'success': False, 'error': 'Price must be a positive number'}), 400
            product.price = float(data['price'])
        
        product.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Product updated: {product.sku} - {product.name}")
        
        # Update metrics
        PRODUCT_OPERATIONS.labels(operation_type='update').inc()
        STOCK_LEVEL_GAUGE.labels(
            product_id=str(product.id), 
            product_name=product.name, 
            sku=product.sku
        ).set(product.stock_level)
        
        # Check for low stock alert
        if product.stock_level <= product.min_stock_threshold:
            LOW_STOCK_ALERTS.labels(
                product_id=str(product.id), 
                product_name=product.name
            ).inc()
        
        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'product': product.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating product {product_id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product from inventory"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Delete associated restock logs first
        RestockLog.query.filter_by(product_id=product_id).delete()
        
        db.session.delete(product)
        db.session.commit()
        
        # Update metrics
        PRODUCT_OPERATIONS.labels(operation_type='delete').inc()
        # Remove stock level gauge for deleted product
        STOCK_LEVEL_GAUGE.labels(
            product_id=str(product.id), 
            product_name=product.name, 
            sku=product.sku
        ).remove()
        
        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Restocking Operations

@app.route('/api/products/<int:product_id>/restock', methods=['POST'])
@limiter.limit("20 per minute")
def restock_product(product_id):
    """Restock a specific product"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({'success': False, 'error': 'Quantity is required'}), 400
        
        # Validate quantity
        if not validate_stock_level(data['quantity']) or int(data['quantity']) <= 0:
            return jsonify({'success': False, 'error': 'Quantity must be a positive integer'}), 400
        
        quantity = int(data['quantity'])
        
        # Store previous stock level
        previous_stock = product.stock_level
        
        # Update stock level
        product.stock_level += quantity
        product.updated_at = datetime.utcnow()
        
        # Create restock log
        restock_log = RestockLog(
            product_id=product_id,
            quantity_added=quantity,
            previous_stock=previous_stock,
            new_stock=product.stock_level,
            notes=data.get('notes', '')[:500]  # Limit notes length
        )
        
        db.session.add(restock_log)
        db.session.commit()
        
        logger.info(f"Product restocked: {product.sku} - Added {quantity} units")
        
        # Update metrics
        RESTOCK_OPERATIONS.labels(
            product_id=str(product.id), 
            product_name=product.name
        ).inc()
        STOCK_LEVEL_GAUGE.labels(
            product_id=str(product.id), 
            product_name=product.name, 
            sku=product.sku
        ).set(product.stock_level)
        
        return jsonify({
            'success': True,
            'message': f'Product restocked successfully. Added {quantity} units.',
            'product': product.to_dict(),
            'restock_log': restock_log.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error restocking product {product_id}: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/restocks', methods=['GET'])
def get_restock_history():
    """Get history of all restocking operations"""
    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Query restock logs with pagination
        restock_logs = RestockLog.query.order_by(RestockLog.restocked_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'restock_logs': [log.to_dict() for log in restock_logs.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': restock_logs.total,
                'pages': restock_logs.pages
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics Endpoints

@app.route('/api/products/low-stock', methods=['GET'])
def get_low_stock_products():
    try:
        low_stock_products = db.session.query(Product).filter(
            Product.stock_level <= Product.min_stock_threshold
        ).all()
        
        products_data = []
        for product in low_stock_products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'quantity': product.stock_level,
                'min_stock_level': product.min_stock_threshold,
                'price': product.price
            })
        
        return jsonify({
            'success': True,
            'products': products_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

    
@app.route('/api/products/analytics', methods=['GET'])
def get_stock_analytics():
    """Get stock analytics and trends"""
    try:
        # Basic analytics
        total_products = Product.query.count()
        low_stock_count = Product.query.filter(
            Product.stock_level <= Product.min_stock_threshold
        ).count()
        
        # Total stock value
        total_stock_value = db.session.query(
            func.sum(Product.stock_level * Product.price)
        ).scalar() or 0
        
        # Recent restocking activity (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_restocks = RestockLog.query.filter(
            RestockLog.restocked_at >= thirty_days_ago
        ).count()
        
        # Top 5 products by stock level
        top_stock_products = Product.query.order_by(Product.stock_level.desc()).limit(5).all()
        
        # Products with zero stock
        out_of_stock_count = Product.query.filter(Product.stock_level == 0).count()
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_products': total_products,
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count,
                'total_stock_value': round(total_stock_value, 2),
                'recent_restocks_30_days': recent_restocks,
                'low_stock_percentage': round((low_stock_count / total_products * 100) if total_products > 0 else 0, 2),
                'top_stock_products': [
                    {
                        'name': product.name,
                        'sku': product.sku,
                        'stock_level': product.stock_level
                    } for product in top_stock_products
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500



if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
