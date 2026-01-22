"""Authentication service"""
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token


class AuthService:
    """Service for handling authentication logic"""
    
    @staticmethod
    def register_user(name, email, password, phone=None, address=None):
        """Register a new user"""
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return None, "User with this email already exists"
        
        # Create new user
        user = User(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def login_user(email, password):
        """Authenticate user and return access token"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return None, None, "Invalid email or password"
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return user, access_token, None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
