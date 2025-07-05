#!/usr/bin/env python3
"""
Script to load sample products into the inventory database
Usage: python3 load_sample_data.py
"""

import json
import os
import psycopg2
from datetime import datetime

def load_sample_products():
    # Read database configuration from environment variables
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'inventory_db'),
        'user': os.getenv('DB_USER', 'inventory_user'),
        'password': os.getenv('DB_PASSWORD', 'inventory_pass')
    }
    
    try:
        # Connect to PostgreSQL database
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Load JSON data
        print("📁 Loading sample products data...")
        with open('sample_products.json', 'r') as file:
            data = json.load(file)
        
        products = data['products']
        print(f"📦 Found {len(products)} products to load")
        
        # Check if products already exist
        cursor.execute("SELECT COUNT(*) FROM products")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            response = input(f"⚠️  Database already contains {existing_count} products. Do you want to:\n"
                           "1. Add new products (keeping existing ones)\n"
                           "2. Clear database and load fresh data\n"
                           "3. Cancel operation\n"
                           "Enter choice (1/2/3): ").strip()
            
            if response == '2':
                print("🗑️  Clearing existing products...")
                cursor.execute("DELETE FROM restock_logs")
                cursor.execute("DELETE FROM products")
                conn.commit()
                print("✅ Database cleared")
            elif response == '3':
                print("❌ Operation cancelled")
                return
            elif response != '1':
                print("❌ Invalid choice. Operation cancelled")
                return
        
        # Insert products
        insert_query = """
        INSERT INTO products (name, sku, description, price, stock_level, min_stock_threshold, category, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (sku) DO NOTHING
        """
        
        loaded_count = 0
        skipped_count = 0
        
        for product in products:
            try:
                cursor.execute(insert_query, (
                    product['name'],
                    product['sku'],
                    product['description'],
                    product['price'],
                    product['stock_level'],
                    product['min_stock_threshold'],
                    product['category'],
                    datetime.now(),
                    datetime.now()
                ))
                
                if cursor.rowcount > 0:
                    loaded_count += 1
                    print(f"✅ Added: {product['name']} (SKU: {product['sku']})")
                else:
                    skipped_count += 1
                    print(f"⏭️  Skipped: {product['name']} (SKU: {product['sku']}) - already exists")
                    
            except Exception as e:
                print(f"❌ Error adding {product['name']}: {str(e)}")
                skipped_count += 1
        
        # Commit changes
        conn.commit()
        
        # Print summary
        print("\n" + "="*50)
        print("📊 SUMMARY")
        print("="*50)
        print(f"✅ Products loaded successfully: {loaded_count}")
        print(f"⏭️  Products skipped (duplicates): {skipped_count}")
        print(f"📦 Total products in database: {existing_count + loaded_count}")
        
        # Show stock status
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN stock_level = 0 THEN 1 ELSE 0 END) as out_of_stock,
                SUM(CASE WHEN stock_level <= min_stock_threshold AND stock_level > 0 THEN 1 ELSE 0 END) as low_stock,
                SUM(CASE WHEN stock_level > min_stock_threshold THEN 1 ELSE 0 END) as in_stock
            FROM products
        """)
        
        total, out_of_stock, low_stock, in_stock = cursor.fetchone()
        
        print(f"\n📈 STOCK STATUS:")
        print(f"   🟢 In Stock: {in_stock}")
        print(f"   🟡 Low Stock: {low_stock}")
        print(f"   🔴 Out of Stock: {out_of_stock}")
        
        print(f"\n🎉 Sample data loaded successfully!")
        print(f"🌐 You can now view the products at: http://localhost:3000/products")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print("❌ Error: sample_products.json file not found!")
        print("   Make sure the JSON file is in the same directory as this script.")
    except json.JSONDecodeError as e:
        print(f"❌ Error reading JSON file: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print("🔐 Database connection closed")

if __name__ == "__main__":
    print("🚀 Inventory Management - Sample Data Loader")
    print("=" * 50)
    load_sample_products()