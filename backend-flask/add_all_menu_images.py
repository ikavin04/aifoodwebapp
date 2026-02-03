"""Add images to all menu items"""
from app import create_app
from app.extensions import db
from app.models import MenuItem

app = create_app()

with app.app_context():
    print("🖼️  Adding images to all menu items...")
    
    # Generic food images by category
    images_by_category = {
        'Pizza': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400',
        'Burger': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
        'Salad': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400',
        'Sides': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400',
        'Sushi': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
        'Appetizer': 'https://images.unsplash.com/photo-1610180473036-b8f2a7dc0f56?w=400',
        'Biryani': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400',
        'Chinese': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400',
        'Curry': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400',
        'Dessert': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400',
        'Rice': 'https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400',
        'Noodles': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400',
        'Tandoori': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400',
        'Seafood': 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=400',
        'Bread': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400',
        'default': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400'
    }
    
    # Get all menu items
    all_items = MenuItem.query.all()
    count = 0
    
    for item in all_items:
        if not item.image_url:
            # Try to match by category
            category = item.category
            if category in images_by_category:
                item.image_url = images_by_category[category]
            else:
                item.image_url = images_by_category['default']
            count += 1
    
    db.session.commit()
    print(f"✅ Added images to {count} menu items")
    print("🎉 All menu items now have images!")
