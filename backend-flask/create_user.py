"""Create a test user for the application"""
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    # Delete existing test user first
    User.query.filter_by(email='test@example.com').delete()
    db.session.commit()
    
    # Create new user
    user = User(
        name='Test User',
        email='test@example.com',
        phone='1234567890'
    )
    user.set_password('password123')
    
    db.session.add(user)
    db.session.commit()
    
    # Verify the user was created and password works
    test_user = User.query.filter_by(email='test@example.com').first()
    print("✅ User created successfully!")
    print(f"Email: test@example.com")
    print(f"Password: password123")
    print(f"Verification: {test_user.check_password('password123')}")

