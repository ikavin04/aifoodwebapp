"""Address management routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.services.address_service import AddressService

address_bp = Blueprint('address', __name__, url_prefix='/addresses')


def get_current_user_id():
    """Helper to get current user ID from JWT or use default"""
    try:
        verify_jwt_in_request(optional=True)
        jwt_identity = get_jwt_identity()
        if jwt_identity is not None:
            return jwt_identity
    except:
        pass
    return 4  # Default fallback user_id


@address_bp.route('', methods=['GET'])
def get_user_addresses():
    """Get all addresses for the current user"""
    try:
        user_id = get_current_user_id()
        addresses = AddressService.get_user_addresses(user_id)
        
        return jsonify({
            'addresses': [addr.to_dict() for addr in addresses],
            'count': len(addresses)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@address_bp.route('', methods=['POST'])
def add_address():
    """Add a new address for the current user"""
    try:
        data = request.get_json()
        user_id = get_current_user_id()
        
        # Validate required fields
        required_fields = ['label', 'address_line1', 'city', 'state', 'pincode']
        missing_fields = []
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'received_data': data
            }), 400
        
        address, error = AddressService.create_address(
            user_id=user_id,
            label=data.get('label'),
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            city=data.get('city'),
            state=data.get('state'),
            pincode=data.get('pincode'),
            landmark=data.get('landmark'),
            phone=data.get('phone'),
            is_default=data.get('is_default', False)
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Address added successfully',
            'address': address.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@address_bp.route('/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    """Update an existing address"""
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        address, error = AddressService.update_address(
            address_id=address_id,
            user_id=user_id,
            **data
        )
        
        if error:
            return jsonify({'error': error, 'debug_info': {'user_id': user_id, 'address_id': address_id}}), 400
        
        return jsonify({
            'message': 'Address updated successfully',
            'address': address.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@address_bp.route('/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    """Delete an address"""
    try:
        user_id = get_current_user_id()
        
        success, error = AddressService.delete_address(address_id, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Address deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@address_bp.route('/<int:address_id>/set-default', methods=['PUT'])
def set_default_address(address_id):
    """Set an address as default"""
    try:
        user_id = get_current_user_id()
        
        address, error = AddressService.set_default_address(address_id, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Default address updated successfully',
            'address': address.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@address_bp.route('/current', methods=['PUT'])
def set_current_address():
    """Set the current active address for browsing restaurants"""
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        address_id = data.get('address_id') if data else None
        
        if not address_id:
            return jsonify({'error': 'address_id is required', 'received_data': data}), 400
        
        success, error = AddressService.set_current_address(user_id, address_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Current address updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
