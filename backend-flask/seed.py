"""Seed script to populate database with sample data"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app
from app.extensions import db
from app.models import User, Restaurant, MenuItem


def seed_database():
    """Seed the database with sample data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("🗑️  Clearing existing data...")
        MenuItem.query.delete()
        Restaurant.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create sample users
        print("👥 Creating sample users...")
        users = [
            User(name="Ashrudi", email="ashrudiv16@gmail.com", phone="9876543210", address="Coimbatore, Tamil Nadu"),
            User(name="John Doe", email="john@example.com", phone="1234567890", address="123 Main St, City"),
            User(name="Jane Smith", email="jane@example.com", phone="0987654321", address="456 Oak Ave, Town"),
            User(name="Test User", email="test@example.com", phone="5555555555", address="789 Pine Rd, Village")
        ]
        
        for user in users:
            # Set custom password for Ashrudi, default for others
            if user.email == "ashrudiv16@gmail.com":
                user.set_password("ashrudi16")
            else:
                user.set_password("password123")
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create sample restaurants - Real Coimbatore Restaurants
        print("🍽️  Creating sample restaurants...")
        restaurants = [
            Restaurant(
                name="Anjappar Chettinad",
                description="Authentic Chettinad cuisine with spicy flavors",
                address="1062, Avinashi Road, Coimbatore",
                phone="0422-4344344",
                image_url="https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400",
                cuisine_type="South Indian",
                rating=4.5,
                delivery_time="35-45 mins"
            ),
            Restaurant(
                name="Haribhavanam",
                description="Traditional South Indian vegetarian meals",
                address="Mettupalayam Road, Coimbatore",
                phone="0422-2211321",
                image_url="https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400",
                cuisine_type="South Indian",
                rating=4.6,
                delivery_time="25-35 mins"
            ),
            Restaurant(
                name="Domino's Pizza",
                description="Fresh pizzas and sides delivered hot",
                address="RS Puram, Coimbatore",
                phone="1800-208-1234",
                image_url="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400",
                cuisine_type="Italian",
                rating=4.2,
                delivery_time="30-40 mins"
            ),
            Restaurant(
                name="KFC Coimbatore",
                description="Finger lickin' good fried chicken",
                address="Brookefields Mall, Coimbatore",
                phone="1800-209-0000",
                image_url="https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=400",
                cuisine_type="Fast Food",
                rating=4.1,
                delivery_time="25-35 mins"
            ),
            Restaurant(
                name="Shree Annapoorna",
                description="Pure vegetarian South Indian restaurant",
                address="East Arokiasamy Road, RS Puram, Coimbatore",
                phone="0422-4345678",
                image_url="https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=400",
                cuisine_type="South Indian",
                rating=4.7,
                delivery_time="30-40 mins"
            ),
            Restaurant(
                name="Burger King",
                description="Flame-grilled burgers and whopper",
                address="Gandhipuram, Coimbatore",
                phone="1800-102-1010",
                image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
                cuisine_type="Fast Food",
                rating=4.0,
                delivery_time="25-35 mins"
            ),
            Restaurant(
                name="Geetha Cafe",
                description="Famous for idli, dosa and filter coffee",
                address="Nehru Street, RS Puram, Coimbatore",
                phone="0422-2541234",
                image_url="https://images.unsplash.com/photo-1630383249896-424e482df921?w=400",
                cuisine_type="South Indian",
                rating=4.5,
                delivery_time="20-30 mins"
            ),
            Restaurant(
                name="That's Y Food",
                description="Multi-cuisine restaurant with North and South Indian",
                address="Avinashi Road, Coimbatore",
                phone="0422-4567890",
                image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400",
                cuisine_type="Multi-Cuisine",
                rating=4.3,
                delivery_time="35-45 mins"
            ),
            Restaurant(
                name="Hotel Junior Kuppanna",
                description="Kongu Nadu special non-veg meals",
                address="Sathy Road, Coimbatore",
                phone="0422-2234567",
                image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400",
                cuisine_type="South Indian",
                rating=4.4,
                delivery_time="30-40 mins"
            ),
            Restaurant(
                name="Subway Coimbatore",
                description="Fresh subs and healthy sandwiches",
                address="Saibaba Colony, Coimbatore",
                phone="1800-102-5454",
                image_url="https://images.unsplash.com/photo-1509722747041-616f39b57569?w=400",
                cuisine_type="Fast Food",
                rating=4.2,
                delivery_time="20-30 mins"
            ),
            Restaurant(
                name="Sree Anandhaas",
                description="Premium sweets and chaats",
                address="Race Course Road, Coimbatore",
                phone="0422-2345678",
                image_url="https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400",
                cuisine_type="South Indian",
                rating=4.6,
                delivery_time="25-35 mins"
            ),
            Restaurant(
                name="Pasta Street",
                description="Italian pastas and continental cuisine",
                address="Peelamedu, Coimbatore",
                phone="0422-3456789",
                image_url="https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400",
                cuisine_type="Italian",
                rating=4.3,
                delivery_time="35-45 mins"
            )
        ]
        
        for restaurant in restaurants:
            db.session.add(restaurant)
        
        db.session.flush()  # Flush to get restaurant IDs before creating menu items
        print(f"✅ Created {len(restaurants)} restaurants")
        
        # Create menu items for each restaurant
        print("📝 Creating menu items...")
        
        # Anjappar Chettinad Menu (Restaurant 1)
        anjappar_items = [
            MenuItem(restaurant_id=restaurants[0].id, name="Chicken Chettinad", description="Spicy chicken curry with Chettinad masala", price=250.00, category="Main Course"),
            MenuItem(restaurant_id=restaurants[0].id, name="Mutton Kola Urundai", description="Spicy mutton meatballs", price=280.00, category="Appetizer"),
            MenuItem(restaurant_id=restaurants[0].id, name="Crab Masala", description="Fresh crab in spicy masala", price=450.00, category="Main Course"),
            MenuItem(restaurant_id=restaurants[0].id, name="Fish Fry", description="Crispy fried fish", price=220.00, category="Appetizer"),
            MenuItem(restaurant_id=restaurants[0].id, name="Meals", description="Traditional Chettinad meals", price=180.00, category="Meals", is_vegetarian=True),
        ]
        
        # Haribhavanam Menu (Restaurant 2)
        haribhavanam_items = [
            MenuItem(restaurant_id=restaurants[1].id, name="Special Meals", description="Unlimited South Indian vegetarian meals", price=150.00, category="Meals", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[1].id, name="Mini Meals", description="Smaller portion meals", price=100.00, category="Meals", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[1].id, name="Ghee Pongal", description="Rice cooked with ghee and spices", price=80.00, category="Main Course", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[1].id, name="Poori Masala", description="Fluffy pooris with potato masala", price=70.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[1].id, name="Filter Coffee", description="Traditional South Indian filter coffee", price=30.00, category="Beverages", is_vegetarian=True),
        ]
        
        # Domino's Pizza Menu (Restaurant 3)
        dominos_items = [
            MenuItem(restaurant_id=restaurants[2].id, name="Margherita Pizza", description="Classic cheese and tomato", price=199.00, category="Pizza", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[2].id, name="Chicken Dominator", description="Loaded with chicken toppings", price=399.00, category="Pizza"),
            MenuItem(restaurant_id=restaurants[2].id, name="Farmhouse Pizza", description="Veggie loaded pizza", price=299.00, category="Pizza", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[2].id, name="Garlic Breadsticks", description="Cheesy garlic breadsticks", price=99.00, category="Sides", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[2].id, name="Choco Lava Cake", description="Hot chocolate lava cake", price=89.00, category="Dessert", is_vegetarian=True),
        ]
        
        # KFC Menu (Restaurant 4)
        kfc_items = [
            MenuItem(restaurant_id=restaurants[3].id, name="Chicken Zinger Burger", description="Spicy crispy chicken burger", price=189.00, category="Burger"),
            MenuItem(restaurant_id=restaurants[3].id, name="Hot & Crispy Chicken", description="Signature fried chicken (3 pcs)", price=279.00, category="Chicken"),
            MenuItem(restaurant_id=restaurants[3].id, name="Bucket Chicken", description="8 pieces of crispy chicken", price=599.00, category="Chicken"),
            MenuItem(restaurant_id=restaurants[3].id, name="Popcorn Chicken", description="Bite-sized chicken pieces", price=169.00, category="Snacks"),
            MenuItem(restaurant_id=restaurants[3].id, name="French Fries", description="Crispy golden fries", price=99.00, category="Sides", is_vegetarian=True),
        ]
        
        # Shree Annapoorna Menu (Restaurant 5)
        annapoorna_items = [
            MenuItem(restaurant_id=restaurants[4].id, name="Full Meals", description="Traditional vegetarian meals", price=140.00, category="Meals", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[4].id, name="Rava Dosa", description="Crispy semolina dosa", price=70.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[4].id, name="Masala Dosa", description="Crispy dosa with potato filling", price=60.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[4].id, name="Idli Sambar", description="Soft idlis with sambar (4 pcs)", price=50.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[4].id, name="Curd Rice", description="Rice with fresh curd", price=50.00, category="Main Course", is_vegetarian=True),
        ]
        
        # Burger King Menu (Restaurant 6)
        bk_items = [
            MenuItem(restaurant_id=restaurants[5].id, name="Whopper", description="Flame-grilled beef whopper", price=199.00, category="Burger"),
            MenuItem(restaurant_id=restaurants[5].id, name="Chicken Whopper", description="Crispy chicken whopper", price=189.00, category="Burger"),
            MenuItem(restaurant_id=restaurants[5].id, name="Veg Whopper", description="Vegetarian whopper", price=149.00, category="Burger", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[5].id, name="Chicken Fries", description="Crispy chicken fries", price=129.00, category="Sides"),
            MenuItem(restaurant_id=restaurants[5].id, name="Onion Rings", description="Crispy onion rings", price=99.00, category="Sides", is_vegetarian=True),
        ]
        
        # Geetha Cafe Menu (Restaurant 7)
        geetha_items = [
            MenuItem(restaurant_id=restaurants[6].id, name="Ghee Roast Dosa", description="Crispy dosa with ghee", price=80.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[6].id, name="Set Dosa", description="Soft dosas (3 pcs)", price=60.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[6].id, name="Pongal", description="Traditional rice dish", price=50.00, category="Breakfast", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[6].id, name="Vada", description="Crispy lentil fritters (2 pcs)", price=35.00, category="Snacks", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[6].id, name="Filter Coffee", description="Strong filter coffee", price=25.00, category="Beverages", is_vegetarian=True),
        ]
        
        # That's Y Food Menu (Restaurant 8)
        thatsy_items = [
            MenuItem(restaurant_id=restaurants[7].id, name="Butter Chicken", description="Creamy tomato chicken curry", price=280.00, category="Main Course"),
            MenuItem(restaurant_id=restaurants[7].id, name="Paneer Butter Masala", description="Cottage cheese in rich gravy", price=240.00, category="Main Course", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[7].id, name="Veg Fried Rice", description="Indo-Chinese fried rice", price=150.00, category="Rice", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[7].id, name="Chicken Biryani", description="Fragrant chicken biryani", price=220.00, category="Biryani"),
            MenuItem(restaurant_id=restaurants[7].id, name="Naan", description="Butter naan (2 pcs)", price=50.00, category="Bread", is_vegetarian=True),
        ]
        
        # Junior Kuppanna Menu (Restaurant 9)
        kuppanna_items = [
            MenuItem(restaurant_id=restaurants[8].id, name="Nattu Kozhi Curry", description="Country chicken curry", price=300.00, category="Main Course"),
            MenuItem(restaurant_id=restaurants[8].id, name="Mutton Biryani", description="Aromatic mutton biryani", price=350.00, category="Biryani"),
            MenuItem(restaurant_id=restaurants[8].id, name="Eral Masala", description="Prawn masala curry", price=320.00, category="Main Course"),
            MenuItem(restaurant_id=restaurants[8].id, name="Non-Veg Meals", description="Traditional non-veg meals", price=220.00, category="Meals"),
            MenuItem(restaurant_id=restaurants[8].id, name="Chicken 65", description="Spicy fried chicken", price=180.00, category="Appetizer"),
        ]
        
        # Subway Menu (Restaurant 10)
        subway_items = [
            MenuItem(restaurant_id=restaurants[9].id, name="Veggie Delite Sub", description="Fresh vegetables sub", price=150.00, category="Sub", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[9].id, name="Chicken Tikka Sub", description="Chicken tikka sub", price=199.00, category="Sub"),
            MenuItem(restaurant_id=restaurants[9].id, name="Paneer Tikka Sub", description="Paneer tikka sub", price=189.00, category="Sub", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[9].id, name="Cookie", description="Chocolate chip cookie", price=50.00, category="Dessert", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[9].id, name="Chips", description="Crispy potato chips", price=40.00, category="Sides", is_vegetarian=True),
        ]
        
        # Sree Anandhaas Menu (Restaurant 11)
        anandhaas_items = [
            MenuItem(restaurant_id=restaurants[10].id, name="Mysore Pak", description="Traditional ghee sweet", price=180.00, category="Sweets", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[10].id, name="Gulab Jamun", description="Soft milk sweet in syrup (4 pcs)", price=80.00, category="Sweets", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[10].id, name="Samosa", description="Crispy samosa (2 pcs)", price=40.00, category="Snacks", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[10].id, name="Pani Puri", description="Street-style pani puri", price=50.00, category="Chaat", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[10].id, name="Dahi Puri", description="Yogurt puri chaat", price=60.00, category="Chaat", is_vegetarian=True),
        ]
        
        # Pasta Street Menu (Restaurant 12)
        pasta_items = [
            MenuItem(restaurant_id=restaurants[11].id, name="Alfredo Pasta", description="Creamy white sauce pasta", price=250.00, category="Pasta", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[11].id, name="Arrabbiata Pasta", description="Spicy tomato pasta", price=240.00, category="Pasta", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[11].id, name="Chicken Pasta", description="Pasta with grilled chicken", price=280.00, category="Pasta"),
            MenuItem(restaurant_id=restaurants[11].id, name="Garlic Bread", description="Toasted garlic bread", price=100.00, category="Sides", is_vegetarian=True),
            MenuItem(restaurant_id=restaurants[11].id, name="Caesar Salad", description="Fresh romaine salad", price=180.00, category="Salad", is_vegetarian=True),
        ]
        
        all_items = anjappar_items + haribhavanam_items + dominos_items + kfc_items + annapoorna_items + bk_items + geetha_items + thatsy_items + kuppanna_items + subway_items + anandhaas_items + pasta_items
        
        for item in all_items:
            db.session.add(item)
        
        db.session.commit()
        print(f"✅ Created {len(all_items)} menu items")
        
        print("✨ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   - {User.query.count()} users")
        print(f"   - {Restaurant.query.count()} restaurants")
        print(f"   - {MenuItem.query.count()} menu items")
        print("\n🔐 Your credentials:")
        print("   Email: ashrudiv16@gmail.com")
        print("   Password: ashrudi16")
        print("\n🔐 Test credentials:")
        print("   Email: test@example.com")
        print("   Password: password123")


if __name__ == '__main__':
    seed_database()
