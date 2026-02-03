"""Add images to all restaurants that don't have them"""
from app import create_app
from app.extensions import db
from app.models import Restaurant

app = create_app()

with app.app_context():
    print("🖼️  Adding images to restaurants...")
    
    # Generic restaurant images by cuisine type
    images_by_cuisine = {
        'South Indian': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
        'Italian': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400',
        'American': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
        'Japanese': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
        'Mughlai': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400',
        'Chinese': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400',
        'North Indian': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400',
        'Kerala': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400',
        'Mexican': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400',
        'Thai': 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400',
        'default': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400'
    }
    
    # Get all restaurants
    restaurants = Restaurant.query.all()
    count = 0
    
    for restaurant in restaurants:
        if not restaurant.image_url:
            # Match by cuisine type
            cuisine = restaurant.cuisine_type
            if cuisine in images_by_cuisine:
                restaurant.image_url = images_by_cuisine[cuisine]
            else:
                restaurant.image_url = images_by_cuisine['default']
            count += 1
            print(f"  → Added image to {restaurant.name} ({cuisine})")
    
    db.session.commit()
    print(f"✅ Added images to {count} restaurants")
    print("🎉 All restaurants now have images!")
