"""Test JWT token validation"""
from app import create_app
from flask_jwt_extended import create_access_token, decode_token

app = create_app('development')

with app.app_context():
    # Create a test token
    test_user_id = 1
    token = create_access_token(identity=test_user_id)
    print(f"Generated token: {token[:50]}...")
    
    # Try to decode it
    try:
        decoded = decode_token(token)
        print(f"Token decoded successfully!")
        print(f"User ID: {decoded['sub']}")
    except Exception as e:
        print(f"Error decoding token: {e}")
    
    # Check config
    print(f"\nJWT Config:")
    print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
