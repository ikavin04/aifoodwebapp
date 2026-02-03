"""Order routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.order_service import OrderService
from app.utils.validators import validate_order

order_bp = Blueprint('orders', __name__, url_prefix='/orders')


@order_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        is_valid, errors = validate_order(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Create order
        order, error = OrderService.create_order(
            user_id=user_id,
            items=data.get('items'),
            delivery_address=data.get('delivery_address'),
            phone=data.get('phone'),
            notes=data.get('notes')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@order_bp.route('/history', methods=['GET'])
@jwt_required()
def get_order_history():
    """Get user's order history"""
    try:
        user_id = get_jwt_identity()
        orders = OrderService.get_user_orders(user_id)
        
        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get a specific order"""
    try:
        user_id = get_jwt_identity()
        order = OrderService.get_order_by_id(order_id, user_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'order': order.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@order_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        user_id = get_jwt_identity()
        order, error = OrderService.cancel_order(order_id, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@order_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (admin only - add role check later)"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        order, error = OrderService.update_order_status(order_id, status)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Order status updated',
            'order': order.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
