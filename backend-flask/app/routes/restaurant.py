"""Restaurant routes"""
from flask import Blueprint, request, jsonify
from app.services.restaurant_service import RestaurantService

restaurant_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')


@restaurant_bp.route('', methods=['GET'])
def get_restaurants():
    """Get all restaurants or search by query"""
    try:
        query = request.args.get('query')
        cuisine_type = request.args.get('cuisine_type')
        
        if query or cuisine_type:
            restaurants = RestaurantService.search_restaurants(query, cuisine_type)
        else:
            restaurants = RestaurantService.get_all_restaurants()
        
        return jsonify({
            'restaurants': [r.to_dict() for r in restaurants],
            'count': len(restaurants)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@restaurant_bp.route('/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    """Get a specific restaurant"""
    try:
        restaurant = RestaurantService.get_restaurant_by_id(restaurant_id)
        
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        return jsonify({'restaurant': restaurant.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@restaurant_bp.route('/<int:restaurant_id>/menu', methods=['GET'])
def get_restaurant_menu(restaurant_id):
    """Get menu items for a specific restaurant"""
    try:
        menu_items, error = RestaurantService.get_restaurant_menu(restaurant_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        return jsonify({
            'menu_items': [item.to_dict() for item in menu_items],
            'count': len(menu_items)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
