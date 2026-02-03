"""Cart service"""
from app.extensions import db
from app.models import Cart, MenuItem


class CartService:
    """Service for handling cart operations"""
    
    @staticmethod
    def add_to_cart(user_id, menu_item_id, quantity=1):
        """Add item to cart or update quantity if exists"""
        # Check if menu item exists and is available
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return None, "Menu item not found"
        
        if not menu_item.is_available:
            return None, "Menu item is not available"
        
        # Check if item already in cart
        cart_item = Cart.query.filter_by(
            user_id=user_id,
            menu_item_id=menu_item_id
        ).first()
        
        try:
            if cart_item:
                # Update quantity
                cart_item.quantity += quantity
            else:
                # Add new item
                cart_item = Cart(
                    user_id=user_id,
                    menu_item_id=menu_item_id,
                    quantity=quantity
                )
                db.session.add(cart_item)
            
            db.session.commit()
            return cart_item, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_user_cart(user_id):
        """Get all cart items for a user"""
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        # Calculate total
        total = sum(item.quantity * item.menu_item.price for item in cart_items if item.menu_item)
        
        return cart_items, total
    
    @staticmethod
    def update_cart_item(user_id, cart_item_id, quantity):
        """Update cart item quantity"""
        cart_item = Cart.query.filter_by(id=cart_item_id, user_id=user_id).first()
        
        if not cart_item:
            return None, "Cart item not found"
        
        try:
            if quantity <= 0:
                db.session.delete(cart_item)
            else:
                cart_item.quantity = quantity
            
            db.session.commit()
            return cart_item, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def remove_from_cart(user_id, cart_item_id):
        """Remove item from cart"""
        cart_item = Cart.query.filter_by(id=cart_item_id, user_id=user_id).first()
        
        if not cart_item:
            return False, "Cart item not found"
        
        try:
            db.session.delete(cart_item)
            db.session.commit()
            return True, None
        
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def clear_cart(user_id):
        """Clear all items from user's cart"""
        try:
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return True, None
        
        except Exception as e:
            db.session.rollback()
            return False, str(e)
