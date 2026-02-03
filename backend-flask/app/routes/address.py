"""Address management routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.address_service import AddressService

address_bp = Blueprint('address', __name__, url_prefix='/addresses')


@address_bp.route('', methods=['GET'])
def get_user_addresses():
    """Get all addresses for the current user"""
    try:
        # Temporary: Try to get user_id from JWT, fallback to query param
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            user_id = request.args.get('user_id', 17)  # Fallback to test user
        
        if not user_id:
            user_id = 17
            
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
        # Temporary: Try to get user_id from JWT, fallback to 17
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            user_id = 17
            
        if not user_id:
            user_id = 17
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['label', 'address_line1', 'city', 'state', 'pincode']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
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
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            user_id = 17
        if not user_id:
            user_id = 17
        data = request.get_json()
        
        address, error = AddressService.update_address(
            address_id=address_id,
            user_id=user_id,
            **data
        )
        
        if error:
            return jsonify({'error': error}), 400
        
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
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            user_id = 17
        if not user_id:
            user_id = 17
        
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
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            user_id = 17
        if not user_id:
            user_id = 17
        
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
        try:
            from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            user_id = 17
        if not user_id:
            user_id = 17
        data = request.get_json()
        
        address_id = data.get('address_id')
        if not address_id:
            return jsonify({'error': 'address_id is required'}), 400
        
        success, error = AddressService.set_current_address(user_id, address_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Current address updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
