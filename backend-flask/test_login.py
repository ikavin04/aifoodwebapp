from app import create_app
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='test@example.com').first()
    if user:
        print(f'User found: {user.email}')
        print(f'Name: {user.name}')
        
        # Test password
        test_passwords = ['password', 'password123', 'Password', 'PASSWORD', 'test', '']
        for pwd in test_passwords:
            result = user.check_password(pwd)
            print(f'Password "{pwd}": {result}')
    else:
        print('User not found!')
