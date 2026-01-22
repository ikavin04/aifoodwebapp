"""Cart routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.cart_service import CartService
from app.utils.validators import validate_cart_item

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart items"""
    try:
        user_id = get_jwt_identity()
        cart_items, total = CartService.get_user_cart(user_id)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total': total,
            'count': len(cart_items)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        is_valid, errors = validate_cart_item(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        cart_item, error = CartService.add_to_cart(
            user_id=user_id,
            menu_item_id=data.get('menu_item_id'),
            quantity=data.get('quantity', 1)
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Item added to cart',
            'cart_item': cart_item.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        quantity = data.get('quantity', 1)
        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        cart_item, error = CartService.update_cart_item(user_id, item_id, quantity)
        
        if error:
            return jsonify({'error': error}), 404
        
        if quantity == 0:
            return jsonify({'message': 'Item removed from cart'}), 200
        
        return jsonify({
            'message': 'Cart updated',
            'cart_item': cart_item.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        user_id = get_jwt_identity()
        success, error = CartService.remove_from_cart(user_id, item_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        return jsonify({'message': 'Item removed from cart'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    try:
        user_id = get_jwt_identity()
        success, error = CartService.clear_cart(user_id)
        
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify({'message': 'Cart cleared'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
