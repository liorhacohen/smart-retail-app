-- Fixed sample data with correct column names
INSERT INTO products (name, sku, description, quantity, min_stock_level, price, category) VALUES
('Laptop Computer', 'LAP001', 'High-performance laptop for business use', 25, 5, 899.99, 'Electronics'),
('Wireless Mouse', 'MSE001', 'Ergonomic wireless mouse with USB receiver', 150, 20, 29.99, 'Electronics'),
('Office Chair', 'CHR001', 'Comfortable ergonomic office chair', 8, 3, 249.99, 'Furniture'),
('USB-C Cable', 'CBL001', '6ft USB-C charging and data cable', 200, 50, 19.99, 'Electronics'),
('Monitor 24inch', 'MON001', '24-inch Full HD LED monitor', 12, 5, 179.99, 'Electronics')
ON CONFLICT (sku) DO NOTHING;
