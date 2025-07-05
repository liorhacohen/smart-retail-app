# Flask Backend for Inventory Management System
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import func

# Initialize Flask app
app = Flask(__name__)

# Database configuration
# Build DATABASE_URL from individual environment variables
db_user = os.getenv('DB_USER', 'inventory_user')
db_password = os.getenv('DB_PASSWORD', 'inventory_pass')
db_host = os.getenv('DB_HOST', 'db')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'inventory_db')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

# Initialize database
db = SQLAlchemy(app)

# Global flag to ensure database tables are created only once
_database_initialized = False

# Database Models
class Product(db.Model):
    """Product model to store product information"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    stock_level = db.Column(db.Integer, default=0)
    min_stock_threshold = db.Column(db.Integer, default=10)  # Low stock alert threshold
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
def create_product():
    """Add a new product to inventory"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('sku'):
            return jsonify({'success': False, 'error': 'Name and SKU are required'}), 400
        
        # Check if SKU already exists
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({'success': False, 'error': 'Product with this SKU already exists'}), 400
        
        # Create new product
        product = Product(
            name=data['name'],
            sku=data['sku'],
            description=data.get('description', ''),
            stock_level=data.get('stock_level', 0),
            min_stock_threshold=data.get('min_stock_threshold', 10),
            price=data.get('price', 0.0)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product details or stock level"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Update product fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'stock_level' in data:
            product.stock_level = data['stock_level']
        if 'min_stock_threshold' in data:
            product.min_stock_threshold = data['min_stock_threshold']
        if 'price' in data:
            product.price = data['price']
        
        product.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'product': product.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product from inventory"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Delete associated restock logs first
        RestockLog.query.filter_by(product_id=product_id).delete()
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Restocking Operations

@app.route('/api/products/<int:product_id>/restock', methods=['POST'])
def restock_product(product_id):
    """Restock a specific product"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({'success': False, 'error': 'Quantity is required'}), 400
        
        quantity = data['quantity']
        if quantity <= 0:
            return jsonify({'success': False, 'error': 'Quantity must be positive'}), 400
        
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
            notes=data.get('notes', '')
        )
        
        db.session.add(restock_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Product restocked successfully. Added {quantity} units.',
            'product': product.to_dict(),
            'restock_log': restock_log.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

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
    """Get products with stock below threshold"""
    try:
        # Query products where stock level is at or below minimum threshold
        low_stock_products = Product.query.filter(
            Product.stock_level <= Product.min_stock_threshold
        ).all()
        
        return jsonify({
            'success': True,
            'low_stock_products': [product.to_dict() for product in low_stock_products],
            'count': len(low_stock_products)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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