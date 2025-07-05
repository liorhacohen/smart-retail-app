-- Database initialization script for Inventory Management System

-- Create database (if using this script outside Docker)
-- CREATE DATABASE inventory_db;

-- Create user and grant privileges
-- This is handled by environment variables in docker-compose

-- Create extension for UUID generation (optional, for future use)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Insert sample data for testing (optional)
-- This will be executed after tables are created by SQLAlchemy

INSERT INTO products (name, sku, description, stock_level, min_stock_threshold, price) VALUES
('Laptop Computer', 'LAP001', 'High-performance laptop for business use', 25, 5, 899.99),
('Wireless Mouse', 'MSE001', 'Ergonomic wireless mouse with USB receiver', 150, 20, 29.99),
('Office Chair', 'CHR001', 'Comfortable ergonomic office chair', 8, 3, 249.99),
('USB-C Cable', 'CBL001', '6ft USB-C charging and data cable', 200, 50, 19.99),
('Monitor 24inch', 'MON001', '24-inch Full HD LED monitor', 12, 5, 179.99),
('Keyboard Mechanical', 'KBD001', 'Mechanical keyboard with RGB backlighting', 35, 10, 79.99),
('Webcam HD', 'CAM001', '1080p HD webcam with built-in microphone', 45, 8, 59.99),
('External Hard Drive', 'HDD001', '1TB portable external hard drive', 18, 5, 89.99),
('Printer Inkjet', 'PRT001', 'Color inkjet printer with wireless connectivity', 6, 2, 129.99),
('Desk Lamp LED', 'LMP001', 'Adjustable LED desk lamp with USB charging port', 22, 5, 39.99)
ON CONFLICT (sku) DO NOTHING;

-- Insert sample restock logs
INSERT INTO restock_logs (product_id, quantity_added, previous_stock, new_stock, notes) VALUES
(1, 10, 15, 25, 'Regular monthly restock'),
(2, 50, 100, 150, 'Bulk order due to high demand'),
(3, 3, 5, 8, 'Low stock emergency restock'),
(4, 100, 100, 200, 'Quarterly bulk purchase'),
(5, 5, 7, 12, 'Restocked after promotion')
ON CONFLICT DO NOTHING;