"""Create a test user for the application"""
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    # Check if user already exists
    existing_user = User.query.filter_by(email='test@example.com').first()
    
    if existing_user:
        print("User already exists!")
        print(f"Email: {existing_user.email}")
        print(f"Name: {existing_user.name}")
    else:
        # Create new user
        user = User(
            name='Test User',
            email='test@example.com',
            phone='1234567890'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        print("✅ User created successfully!")
        print(f"Email: test@example.com")
        print(f"Password: password123")
        print(f"Name: {user.name}")
