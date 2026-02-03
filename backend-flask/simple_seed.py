"""Simple seed script to populate database with sample data"""
from app import create_app
from app.extensions import db
from app.models import User, Restaurant, MenuItem

app = create_app()

with app.app_context():
    print("🌱 Seeding database...")
    
    # Create or update test user
    user = User.query.filter_by(email="test@example.com").first()
    if user:
        user.set_password("password123")
        print("✅ Updated test user password (email: test@example.com, password: password123)")
    else:
        user = User(name="Test User", email="test@example.com", phone="1234567890")
        user.set_password("password123")
        db.session.add(user)
        print("✅ Created test user (email: test@example.com, password: password123)")
    
    # Create sample restaurants
    if Restaurant.query.count() == 0:
        restaurants_data = [
            {
                'name': 'Pizza Palace',
                'description': 'Best pizza in town',
                'address': '123 Main St',
                'city': 'Coimbatore',
                'state': 'Tamil Nadu',
                'pincode': '641001',
                'phone': '0422-1234567',
                'cuisine_type': 'Italian',
                'rating': 4.5,
                'delivery_time': '30-40 mins',
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400'
            },
            {
                'name': 'Burger Hub',
                'description': 'Juicy burgers and fries',
                'address': '456 Park Ave',
                'city': 'Coimbatore',
                'state': 'Tamil Nadu',
                'pincode': '641002',
                'phone': '0422-2345678',
                'cuisine_type': 'American',
                'rating': 4.2,
                'delivery_time': '25-35 mins',
                'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'
            },
            {
                'name': 'Sushi World',
                'description': 'Fresh sushi and Japanese cuisine',
                'address': '789 Ocean Drive',
                'city': 'Coimbatore',
                'state': 'Tamil Nadu',
                'pincode': '641003',
                'phone': '0422-3456789',
                'cuisine_type': 'Japanese',
                'rating': 4.7,
                'delivery_time': '35-45 mins',
                'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400'
            }
        ]
        
        for restaurant_data in restaurants_data:
            restaurant = Restaurant(**restaurant_data)
            db.session.add(restaurant)
            db.session.flush()
            
            # Add sample menu items for each restaurant
            if restaurant.name == 'Pizza Palace':
                menu_items = [
                    {'name': 'Margherita Pizza', 'description': 'Classic pizza with tomato and mozzarella', 'price': 12.99, 'category': 'Pizza', 'is_vegetarian': True},
                    {'name': 'Pepperoni Pizza', 'description': 'Pizza with pepperoni and cheese', 'price': 14.99, 'category': 'Pizza', 'is_vegetarian': False},
                    {'name': 'Caesar Salad', 'description': 'Fresh romaine lettuce with Caesar dressing', 'price': 7.99, 'category': 'Salad', 'is_vegetarian': True}
                ]
            elif restaurant.name == 'Burger Hub':
                menu_items = [
                    {'name': 'Classic Burger', 'description': 'Beef patty with lettuce and tomato', 'price': 9.99, 'category': 'Burger', 'is_vegetarian': False},
                    {'name': 'Veggie Burger', 'description': 'Plant-based patty with fresh veggies', 'price': 8.99, 'category': 'Burger', 'is_vegetarian': True},
                    {'name': 'French Fries', 'description': 'Crispy golden fries', 'price': 3.99, 'category': 'Sides', 'is_vegetarian': True}
                ]
            else:  # Sushi World
                menu_items = [
                    {'name': 'California Roll', 'description': 'Crab, avocado, and cucumber roll', 'price': 11.99, 'category': 'Sushi', 'is_vegetarian': False},
                    {'name': 'Salmon Nigiri', 'description': 'Fresh salmon on rice', 'price': 13.99, 'category': 'Sushi', 'is_vegetarian': False},
                    {'name': 'Vegetable Tempura', 'description': 'Crispy battered vegetables', 'price': 8.99, 'category': 'Appetizer', 'is_vegetarian': True}
                ]
            
            for item_data in menu_items:
                item = MenuItem(restaurant_id=restaurant.id, **item_data)
                db.session.add(item)
        
        print("✅ Created 3 restaurants with menu items")
    
    db.session.commit()
    print("🎉 Database seeded successfully!")
