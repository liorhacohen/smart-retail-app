# Enhanced app.py with Prometheus metrics - ADD THESE IMPORTS AND CODE

# Add these imports at the top
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Add these metrics after your Flask app initialization
REQUEST_COUNT = Counter(
    'flask_request_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'flask_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

REQUEST_EXCEPTIONS = Counter(
    'flask_request_exceptions_total',
    'Total number of HTTP request exceptions',
    ['method', 'endpoint', 'exception']
)

# Business metrics
INVENTORY_TOTAL_PRODUCTS = Gauge('inventory_total_products', 'Total number of products')
INVENTORY_TOTAL_VALUE = Gauge('inventory_total_value', 'Total inventory value')
INVENTORY_LOW_STOCK_PRODUCTS = Gauge('inventory_low_stock_products', 'Low stock products')
INVENTORY_OUT_OF_STOCK_PRODUCTS = Gauge('inventory_out_of_stock_products', 'Out of stock products')
INVENTORY_IN_STOCK_PRODUCTS = Gauge('inventory_in_stock_products', 'In stock products')
INVENTORY_RECENT_RESTOCKS = Gauge('inventory_recent_restocks', 'Recent restocks (7 days)')

# Add these middleware functions
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request  
def after_request(response):
    request_duration = time.time() - request.start_time
    endpoint = request.endpoint or 'unknown'
    method = request.method
    status_code = response.status_code
    
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(request_duration)
    
    # Update business metrics every 10th request
    if REQUEST_COUNT._value._value % 10 == 0:
        update_business_metrics()
    
    return response

def update_business_metrics():
    """Update business metrics"""
    try:
        total_products = Product.query.count()
        INVENTORY_TOTAL_PRODUCTS.set(total_products)
        
        low_stock_count = Product.query.filter(
            Product.stock_level <= Product.min_stock_threshold,
            Product.stock_level > 0
        ).count()
        
        out_of_stock_count = Product.query.filter(Product.stock_level == 0).count()
        in_stock_count = total_products - low_stock_count - out_of_stock_count
        
        INVENTORY_LOW_STOCK_PRODUCTS.set(low_stock_count)
        INVENTORY_OUT_OF_STOCK_PRODUCTS.set(out_of_stock_count) 
        INVENTORY_IN_STOCK_PRODUCTS.set(in_stock_count)
        
        total_value = db.session.query(func.sum(Product.stock_level * Product.price)).scalar() or 0
        INVENTORY_TOTAL_VALUE.set(float(total_value))
        
    except Exception as e:
        print(f"Error updating metrics: {e}")

# Add this metrics endpoint
@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    update_business_metrics()
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
