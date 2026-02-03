from app import create_app
from app.models import User
from app.extensions import db

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f'\nTotal users in database: {len(users)}\n')
    
    for user in users:
        print(f'ID: {user.id}')
        print(f'Email: {user.email}')
        print(f'Name: {user.name}')
        print('-' * 40)
    
    # Delete all users and create fresh one
    print("\nDeleting all users and creating fresh test user...")
    User.query.delete()
    db.session.commit()
    
    # Create new test user
    new_user = User(
        name='Test User',
        email='test@example.com',
        phone='1234567890'
    )
    new_user.set_password('password123')
    db.session.add(new_user)
    db.session.commit()
    
    print(f"\nNew user created:")
    print(f"ID: {new_user.id}")
    print(f"Email: {new_user.email}")
    print(f"Name: {new_user.name}")
    print("\nYou can now login with:")
    print("Email: test@example.com")
    print("Password: password123")
