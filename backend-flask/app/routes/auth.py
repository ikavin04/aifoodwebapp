"""Authentication routes"""
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import validate_register, validate_login
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, errors = validate_register(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Register user
        user, error = AuthService.register_user(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return access token"""
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, errors = validate_login(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Authenticate user
        user, access_token, error = AuthService.login_user(
            email=data.get('email'),
            password=data.get('password')
        )
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
