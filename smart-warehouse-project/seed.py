# File: seed.py (Upgraded Version)

import psycopg2
import os
import random
from datetime import datetime, timedelta

# --- Richer, More Randomized Configuration ---
NUM_SUPPLIERS = 10
NUM_LOCATIONS = 50
NUM_PRODUCTS = 100
NUM_TRANSACTIONS = 500  # More transactions

SUPPLIERS = [
    ("Global Tech Inc.", "sales@globaltech.com"), ("Precision Parts Ltd.", "contact@precisionparts.com"),
    ("Quantum Solutions", "info@quantumsol.com"), ("Stellar Components", "support@stellarcomp.com"),
    ("Apex Industrial", "orders@apexind.com"), ("Nexus Materials", "materials@nexus.com"),
    ("Synergy Supplies", "supply@synergy.com"), ("Dynamic Devices", "devices@dynamic.com"),
    ("Innovate Systems", "innovate@isystems.com"), ("Core Manufacturing", "core@mfg.com")
]

PRODUCT_DATA = {
    "Electronics": {
        "brands": ["Sony", "Samsung", "LG", "Apple"],
        "items": ["Microcontroller", "Sensor Array", "Display Panel", "Power Unit", "Logic Board"]
    },
    "Mechanical": {
        "brands": ["Bosch", "3M", "SKF", "Apex"],
        "items": ["Bearing Assembly", "Gear Set", "Casing", "Mounting Bracket", "Fastener Kit"]
    },
    "Consumables": {
        "brands": ["Loctite", "WD-40", "Kimtech"],
        "items": ["Adhesive", "Lubricant", "Cleaning Wipes", "Solder Wire", "Thermal Paste"]
    }
}

def get_db_connection():
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_DATABASE"), user=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD"), host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT", "5432")
        )
        print("Connection successful!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to database: {e}")
        return None

def seed_suppliers(cur):
    print("Seeding suppliers...")
    cur.executemany("INSERT INTO suppliers (name, contact_email) VALUES (%s, %s)", SUPPLIERS)
    cur.execute("SELECT id FROM suppliers")
    return [row[0] for row in cur.fetchall()]

def seed_locations(cur):
    print("Seeding locations...")
    locations = []
    for _ in range(NUM_LOCATIONS):
        locations.append((random.randint(1, 10), chr(random.randint(65, 70)), random.randint(1, 20)))
    
    # Use a set to ensure uniqueness
    unique_locations = list(set(locations))
    cur.executemany("INSERT INTO locations (aisle, shelf, bin) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", unique_locations)
    cur.execute("SELECT id FROM locations")
    return [row[0] for row in cur.fetchall()]

def seed_products(cur, supplier_ids):
    print("Seeding products...")
    products = []
    for i in range(NUM_PRODUCTS):
        category = random.choice(list(PRODUCT_DATA.keys()))
        brand = random.choice(PRODUCT_DATA[category]["brands"])
        item = random.choice(PRODUCT_DATA[category]["items"])
        name = f"{brand} {item}"
        sku = f"{category[:3].upper()}-{brand[:3].upper()}-{str(i).zfill(4)}"
        price = round(random.uniform(5.50, 500.99), 2)
        supplier_id = random.choice(supplier_ids)
        products.append((sku, name, f"A high-quality {name}", category, brand, price, supplier_id))

    cur.executemany(
        """
        INSERT INTO products (sku, name, description, category, brand, unit_price, supplier_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, products
    )
    cur.execute("SELECT id FROM products")
    return [row[0] for row in cur.fetchall()]

def seed_inventory_transactions(cur, product_ids, location_ids):
    print(f"Seeding {NUM_TRANSACTIONS} transactions with stock simulation...")
    stock_levels = {product_id: 0 for product_id in product_ids}
    transactions = []

    for _ in range(NUM_TRANSACTIONS):
        product_id = random.choice(product_ids)
        current_stock = stock_levels[product_id]
        
        # Decide if it's an IN or OUT transaction
        # Make IN more likely if stock is low, OUT more likely if stock is high
        if current_stock < 10 or random.random() < 0.6:
            status = "IN"
            quantity = random.randint(10, 200)
            stock_levels[product_id] += quantity
        else:
            status = "OUT"
            # Ensure we don't ship more than we have
            if current_stock > 0:
                quantity = random.randint(1, current_stock)
                stock_levels[product_id] -= quantity
            else:
                continue # Skip this transaction if stock is zero

        location_id = random.choice(location_ids)
        scanned_at = datetime.now() - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        transactions.append((product_id, location_id, quantity, status, scanned_at))

    cur.executemany(
        """
        INSERT INTO inventory_transactions (product_id, location_id, quantity, status, scanned_at) 
        VALUES (%s, %s, %s, %s, %s)
        """, transactions
    )

def main():
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # Seed in order of dependency
            supplier_ids = seed_suppliers(cur)
            location_ids = seed_locations(cur)
            product_ids = seed_products(cur, supplier_ids)
            seed_inventory_transactions(cur, product_ids, location_ids)
            
            print("All tables seeded successfully.")
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    main()