"""Debug script to test login"""
from app import create_app
from app.models import User
from app.services.auth_service import AuthService

app = create_app()

with app.app_context():
    email = "test@example.com"
    password = "password123"
    
    print(f"Testing login for: {email}")
    print(f"Password: {password}")
    print()
    
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        print("❌ User not found!")
    else:
        print(f"✅ User found: {user.email}")
        print(f"   Name: {user.name}")
        
        # Test password
        password_check = user.check_password(password)
        print(f"   Password check: {password_check}")
        
        if password_check:
            # Try login service
            user_result, token, error = AuthService.login_user(email, password)
            if error:
                print(f"❌ Login service error: {error}")
            else:
                print(f"✅ Login successful!")
                print(f"   Token: {token[:50]}...")
        else:
            print(f"❌ Password is incorrect!")
            
            # Try other passwords
            print("\nTrying other passwords:")
            for pwd in ['password', 'Password', 'test123']:
                result = user.check_password(pwd)
                print(f"   '{pwd}': {result}")
