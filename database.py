"""
Database connection module for PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os


# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'food_ordering_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}


def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise


def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create restaurants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address TEXT,
            rating DECIMAL(2,1) DEFAULT 0.0,
            distance_km DECIMAL(5,2) DEFAULT 0.0,
            delivery_fee DECIMAL(10,2) DEFAULT 0.0,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create menu_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id SERIAL PRIMARY KEY,
            restaurant_id INTEGER REFERENCES restaurants(id),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category VARCHAR(100),
            is_veg BOOLEAN DEFAULT true,
            is_available BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER REFERENCES restaurants(id),
            total_amount DECIMAL(10,2) NOT NULL,
            delivery_fee DECIMAL(10,2) DEFAULT 0.0,
            payment_method VARCHAR(50) DEFAULT 'COD',
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            menu_item_id INTEGER REFERENCES menu_items(id),
            quantity INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Database initialized successfully!")


def seed_sample_data():
    """Insert sample data for testing"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Sample restaurants
    restaurants = [
        ("Paradise Biryani", "Banjara Hills, Hyderabad", 4.5, 2.5, 30),
        ("Domino's Pizza", "Jubilee Hills, Hyderabad", 4.2, 1.8, 25),
        ("Mehfil Restaurant", "Ameerpet, Hyderabad", 4.7, 3.0, 35),
        ("Food Court Express", "Kukatpally, Hyderabad", 4.0, 4.5, 40),
        ("Royal Biryani House", "Madhapur, Hyderabad", 4.6, 2.0, 28)
    ]
    
    for rest in restaurants:
        cursor.execute("""
            INSERT INTO restaurants (name, address, rating, distance_km, delivery_fee)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, rest)
    
    # Sample menu items
    menu_items = [
        # Paradise Biryani
        (1, "Chicken Biryani", "Authentic Hyderabadi biryani", 180, "Main Course", False),
        (1, "Veg Biryani", "Vegetable biryani with raita", 150, "Main Course", True),
        (1, "Mutton Biryani", "Premium mutton biryani", 250, "Main Course", False),
        
        # Domino's
        (2, "Margherita Pizza", "Classic cheese pizza", 199, "Pizza", True),
        (2, "Chicken Pepperoni", "Spicy pepperoni pizza", 299, "Pizza", False),
        (2, "Veg Supreme", "Loaded veg pizza", 249, "Pizza", True),
        
        # Mehfil
        (3, "Special Biryani", "Chef's special biryani", 170, "Main Course", False),
        (3, "Paneer Biryani", "Paneer and rice delicacy", 160, "Main Course", True),
        
        # Food Court Express
        (4, "Budget Biryani", "Economical biryani", 120, "Main Course", False),
        (4, "Mini Chicken Biryani", "Small portion biryani", 90, "Main Course", False),
        
        # Royal Biryani House
        (5, "Royal Chicken Biryani", "Premium quality biryani", 195, "Main Course", False),
        (5, "Hyderabadi Veg Biryani", "Traditional veg biryani", 145, "Main Course", True)
    ]
    
    for item in menu_items:
        cursor.execute("""
            INSERT INTO menu_items (restaurant_id, name, description, price, category, is_veg)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, item)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Sample data seeded successfully!")


if __name__ == '__main__':
    init_db()
    seed_sample_data()
