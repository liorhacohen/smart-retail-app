# Import phase
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Te%25m%25Fj4fQye2S%2AA@localhost:5432/inventory_db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    stock = db.Column(db.Integer, default=0)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'sku': p.sku, 'stock': p.stock} for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'sku': product.sku, 'stock': product.stock})

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], sku=data['sku'], stock=data.get('stock', 0))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added!'}), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.sku = data.get('sku', product.sku)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({'message': 'Product updated!'})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted!'})

@app.route('/api/products/<int:product_id>/restock', methods=['POST'])
def restock_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    quantity = data.get('quantity', 0)
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be positive'}), 400
    product.stock += quantity
    db.session.commit()
    return jsonify({'message': f'Product {product.name} restocked with {quantity} units. New stock: {product.stock}'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# ------------- End of application code

#