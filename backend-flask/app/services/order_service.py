"""Order service"""
from app.extensions import db
from app.models import Order, OrderItem, MenuItem, Cart


class OrderService:
    """Service for handling order operations"""
    
    @staticmethod
    def create_order(user_id, items, delivery_address, phone, notes=None, payment_method='cash_on_delivery'):
        """Create a new order"""
        if not items or len(items) == 0:
            return None, "No items provided"
        
        # Validate all items and calculate total
        order_items_data = []
        total_amount = 0
        restaurant_id = None
        
        for item_data in items:
            menu_item = MenuItem.query.get(item_data.get('menu_item_id'))
            
            if not menu_item:
                return None, f"Menu item {item_data.get('menu_item_id')} not found"
            
            if not menu_item.is_available:
                return None, f"Menu item '{menu_item.name}' is not available"
            
            # All items must be from the same restaurant
            if restaurant_id is None:
                restaurant_id = menu_item.restaurant_id
            elif restaurant_id != menu_item.restaurant_id:
                return None, "All items must be from the same restaurant"
            
            quantity = item_data.get('quantity', 1)
            subtotal = menu_item.price * quantity
            total_amount += subtotal
            
            order_items_data.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'price': menu_item.price
            })
        
        # Create order
        try:
            order = Order(
                user_id=user_id,
                restaurant_id=restaurant_id,
                total_amount=total_amount,
                delivery_address=delivery_address,
                phone=phone,
                notes=notes,
                status='pending',
                payment_method=payment_method
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=item_data['menu_item'].id,
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Clear user's cart after successful order
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            
            return order, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def get_order_by_id(order_id, user_id=None):
        """Get order by ID, optionally filtered by user"""
        if user_id:
            return Order.query.filter_by(id=order_id, user_id=user_id).first()
        return Order.query.get(order_id)
    
    @staticmethod
    def update_order_status(order_id, status):
        """Update order status"""
        valid_statuses = ['pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled']
        
        if status not in valid_statuses:
            return None, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        
        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"
        
        try:
            order.status = status
            db.session.commit()
            return order, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def cancel_order(order_id, user_id):
        """Cancel an order (only if pending or confirmed)"""
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return None, "Order not found"
        
        if order.status not in ['pending', 'confirmed']:
            return None, f"Cannot cancel order with status '{order.status}'"
        
        try:
            order.status = 'cancelled'
            db.session.commit()
            return order, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
