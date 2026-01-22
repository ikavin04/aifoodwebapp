"""Restaurant service"""
from app.extensions import db
from app.models import Restaurant, MenuItem


class RestaurantService:
    """Service for handling restaurant operations"""
    
    @staticmethod
    def get_all_restaurants():
        """Get all active restaurants"""
        return Restaurant.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        """Get restaurant by ID"""
        return Restaurant.query.get(restaurant_id)
    
    @staticmethod
    def get_restaurant_menu(restaurant_id):
        """Get menu items for a specific restaurant"""
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return None, "Restaurant not found"
        
        menu_items = MenuItem.query.filter_by(
            restaurant_id=restaurant_id,
            is_available=True
        ).all()
        
        return menu_items, None
    
    @staticmethod
    def search_restaurants(query=None, cuisine_type=None):
        """Search restaurants by name or cuisine type"""
        filters = [Restaurant.is_active == True]
        
        if query:
            filters.append(Restaurant.name.ilike(f'%{query}%'))
        
        if cuisine_type:
            filters.append(Restaurant.cuisine_type == cuisine_type)
        
        return Restaurant.query.filter(*filters).all()
