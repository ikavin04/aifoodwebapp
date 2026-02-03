"""Address service for managing user addresses"""
from app.extensions import db
from app.models import User, UserAddress


class AddressService:
    """Service for handling address management logic"""
    
    @staticmethod
    def get_user_addresses(user_id):
        """Get all addresses for a user"""
        return UserAddress.query.filter_by(user_id=user_id).order_by(UserAddress.is_default.desc(), UserAddress.created_at.desc()).all()
    
    @staticmethod
    def create_address(user_id, label, address_line1, city, state, pincode, 
                      address_line2=None, landmark=None, phone=None, is_default=False):
        """Create a new address for a user"""
        try:
            # If this is the first address or is_default is True, set it as default
            existing_addresses = UserAddress.query.filter_by(user_id=user_id).count()
            if existing_addresses == 0:
                is_default = True
            
            # If setting as default, unset other defaults
            if is_default:
                UserAddress.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
            
            address = UserAddress(
                user_id=user_id,
                label=label,
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                pincode=pincode,
                landmark=landmark,
                phone=phone,
                is_default=is_default
            )
            
            db.session.add(address)
            
            # Set as current address if it's the first one
            if existing_addresses == 0:
                user = User.query.get(user_id)
                db.session.flush()  # Flush to get the address ID
                user.current_address_id = address.id
            
            db.session.commit()
            return address, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_address(address_id, user_id, **kwargs):
        """Update an existing address"""
        try:
            address = UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
            
            if not address:
                return None, "Address not found or unauthorized"
            
            # If setting as default, unset other defaults
            if kwargs.get('is_default'):
                UserAddress.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(address, key) and value is not None:
                    setattr(address, key, value)
            
            db.session.commit()
            return address, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_address(address_id, user_id):
        """Delete an address"""
        try:
            address = UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
            
            if not address:
                return False, "Address not found or unauthorized"
            
            # Check if this is the current address
            user = User.query.get(user_id)
            if user.current_address_id == address_id:
                # Set another address as current if available
                other_address = UserAddress.query.filter(
                    UserAddress.user_id == user_id,
                    UserAddress.id != address_id
                ).first()
                user.current_address_id = other_address.id if other_address else None
            
            db.session.delete(address)
            db.session.commit()
            return True, None
        
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def set_default_address(address_id, user_id):
        """Set an address as default"""
        try:
            address = UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
            
            if not address:
                return None, "Address not found or unauthorized"
            
            # Unset other defaults
            UserAddress.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
            address.is_default = True
            
            db.session.commit()
            return address, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def set_current_address(user_id, address_id):
        """Set the current active address for a user"""
        try:
            # Verify address belongs to user
            address = UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
            
            if not address:
                return False, "Address not found or unauthorized"
            
            user = User.query.get(user_id)
            user.current_address_id = address_id
            
            db.session.commit()
            return True, None
        
        except Exception as e:
            db.session.rollback()
            return False, str(e)
