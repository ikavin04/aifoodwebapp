"""Update menu item images"""
from app import create_app
from app.extensions import db
from app.models import MenuItem, Restaurant

app = create_app()

with app.app_context():
    print("🖼️  Updating menu item images...")
    
    # Get all restaurants
    pizza_palace = Restaurant.query.filter_by(name='Pizza Palace').first()
    burger_hub = Restaurant.query.filter_by(name='Burger Hub').first()
    sushi_world = Restaurant.query.filter_by(name='Sushi World').first()
    
    if pizza_palace:
        items = MenuItem.query.filter_by(restaurant_id=pizza_palace.id).all()
        for item in items:
            if item.name == 'Margherita Pizza':
                item.image_url = 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400'
            elif item.name == 'Pepperoni Pizza':
                item.image_url = 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400'
            elif item.name == 'Caesar Salad':
                item.image_url = 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400'
        print(f"✅ Updated {len(items)} Pizza Palace menu items")
    
    if burger_hub:
        items = MenuItem.query.filter_by(restaurant_id=burger_hub.id).all()
        for item in items:
            if item.name == 'Classic Burger':
                item.image_url = 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'
            elif item.name == 'Veggie Burger':
                item.image_url = 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400'
            elif item.name == 'French Fries':
                item.image_url = 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400'
        print(f"✅ Updated {len(items)} Burger Hub menu items")
    
    if sushi_world:
        items = MenuItem.query.filter_by(restaurant_id=sushi_world.id).all()
        for item in items:
            if item.name == 'California Roll':
                item.image_url = 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400'
            elif item.name == 'Salmon Nigiri':
                item.image_url = 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=400'
            elif item.name == 'Vegetable Tempura':
                item.image_url = 'https://images.unsplash.com/photo-1610180473036-b8f2a7dc0f56?w=400'
        print(f"✅ Updated {len(items)} Sushi World menu items")
    
    db.session.commit()
    print("🎉 All menu item images updated successfully!")
