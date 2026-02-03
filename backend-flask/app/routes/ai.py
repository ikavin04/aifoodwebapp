"""AI Assistant routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models import Restaurant, MenuItem, User
from app.extensions import db
import re

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/order-assistant', methods=['POST'])
def order_assistant():
    """AI order assistant endpoint - Works with or without authentication"""
    try:
        # Try to get user_id if authenticated, otherwise use None for guest users
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        data = request.get_json()
        
        message = data.get('message', '')
        
        # For guest users, provide informational responses only
        if not user_id:
            order_intent = parse_order_intent(message)
            if order_intent and order_intent.get('action') == 'place_order':
                return jsonify({
                    'error': 'Please log in or register to place orders! 🔐\n\nYou can browse restaurants and menus, but ordering requires an account.',
                    'need_login': True
                }), 200
            
            # Provide general AI responses for guest users
            response_message = generate_ai_response(message)
            return jsonify({
                'response': response_message,
                'suggestions': []
            }), 200
        
        # For authenticated users, process orders
        # Check if this is an order placement request
        order_intent = parse_order_intent(message)
        
        if order_intent and order_intent.get('action') == 'place_order':
            # Process the order
            result = process_ai_order(user_id, order_intent)
            return jsonify(result), 200 if 'order' in result else 400
        
        # Simple AI response logic
        response_message = generate_ai_response(message)
        
        return jsonify({
            'response': response_message,
            'suggestions': []
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


def parse_order_intent(message):
    """Parse user message to detect order placement intent - Enhanced with location detection"""
    message_lower = message.lower()
    
    # Check for order placement keywords
    order_keywords = ['place order', 'order', 'buy', 'get me', 'i want to order', 'deliver', 'order this']
    has_order_intent = any(keyword in message_lower for keyword in order_keywords)
    
    # Extract dish name - improved pattern to match ANY dish name
    dish_name = None
    restaurant_name = None
    location = None
    
    # Pattern 1: [dish] from [restaurant] [location]
    # Example: "Hot & Crispy Chicken from KFC Coimbatore"
    dish_pattern_1 = r'([a-zA-Z0-9\s&\-]+?)\s+(?:from|at)\s+([a-zA-Z\s]+?)(?:\s+([a-zA-Z\s]+?))?(?:\s+place order|\s+order|\s+with|$)'
    dish_match = re.search(dish_pattern_1, message, re.IGNORECASE)
    if dish_match:
        dish_name = dish_match.group(1).strip()
        # Check if location is in the restaurant name (e.g., "KFC Coimbatore")
        rest_with_loc = dish_match.group(2).strip()
        words = rest_with_loc.split()
        if len(words) > 1 and words[-1][0].isupper():  # Last word likely a location
            restaurant_name = ' '.join(words[:-1])
            location = words[-1]
        else:
            restaurant_name = rest_with_loc
            if dish_match.group(3):
                location = dish_match.group(3).strip()
    
    # Pattern 2: order [dish] from [restaurant]
    if not dish_name:
        dish_pattern_2 = r'order\s+([a-zA-Z0-9\s&\-]+?)\s+from\s+([a-zA-Z\s]+)'
        dish_match = re.search(dish_pattern_2, message, re.IGNORECASE)
        if dish_match:
            dish_name = dish_match.group(1).strip()
            rest_with_loc = dish_match.group(2).strip()
            words = rest_with_loc.split()
            if len(words) > 1 and words[-1][0].isupper():
                restaurant_name = ' '.join(words[:-1])
                location = words[-1]
            else:
                restaurant_name = rest_with_loc
    
    # Extract payment method
    payment_method = None
    if 'cash' in message_lower or 'cod' in message_lower or 'cash on delivery' in message_lower:
        payment_method = 'cash_on_delivery'
    elif 'card' in message_lower or 'credit' in message_lower or 'debit' in message_lower:
        payment_method = 'card'
    elif 'upi' in message_lower or 'online' in message_lower:
        payment_method = 'online'
    
    # Only return intent if we have at least a dish name
    if dish_name or has_order_intent:
        return {
            'action': 'place_order' if has_order_intent else 'query',
            'dish_name': dish_name,
            'restaurant_name': restaurant_name,
            'location': location,
            'payment_method': payment_method,
            'original_message': message
        }
    
    return None


def process_ai_order(user_id, order_intent):
    """Process AI order placement - Enhanced with strict validation"""
    from app.services.order_service import OrderService
    
    # Get user details
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}
    
    # Check for missing information
    missing_info = []
    if not order_intent.get('dish_name'):
        missing_info.append('dish name')
    if not order_intent.get('restaurant_name'):
        missing_info.append('restaurant')
    if not order_intent.get('location'):
        missing_info.append('location')
    
    if missing_info:
        return {
            'error': f"Please provide the {', '.join(missing_info)} for your order.",
            'need_clarification': True,
            'missing': missing_info
        }
    
    # Find restaurant with location filter
    restaurant = None
    location = order_intent.get('location', '').strip()
    restaurant_name = order_intent['restaurant_name'].strip()
    
    if restaurant_name and location:
        # Try exact match first (restaurant + location)
        restaurant = Restaurant.query.filter(
            Restaurant.name.ilike(f"%{restaurant_name}%"),
            Restaurant.location.ilike(f"%{location}%")
        ).first()
        
        if not restaurant:
            # Try restaurant name alone
            restaurant = Restaurant.query.filter(
                Restaurant.name.ilike(f"%{restaurant_name}%")
            ).first()
    elif restaurant_name:
        restaurant = Restaurant.query.filter(
            Restaurant.name.ilike(f"%{restaurant_name}%")
        ).first()
    
    # Find menu item
    menu_item = None
    dish_name = order_intent['dish_name'].strip()
    
    if dish_name and restaurant:
        # Search in specific restaurant
        menu_item = MenuItem.query.filter(
            MenuItem.name.ilike(f"%{dish_name}%"),
            MenuItem.restaurant_id == restaurant.id,
            MenuItem.is_available == True
        ).first()
        
        # If not found, report unavailability
        if not menu_item:
            unavailable_item = MenuItem.query.filter(
                MenuItem.name.ilike(f"%{dish_name}%"),
                MenuItem.restaurant_id == restaurant.id
            ).first()
            
            if unavailable_item and not unavailable_item.is_available:
                return {
                    'error': f"Sorry! {dish_name.title()} is currently unavailable at {restaurant.name}, {location} 😕\nWant to try another item from the same outlet or a different {restaurant.name} nearby?",
                    'unavailable': True,
                    'restaurant': restaurant.name,
                    'location': location
                }
            else:
                return {
                    'error': f"Sorry! {dish_name.title()} is not available at {restaurant.name}, {location} 😕\nWould you like to try another dish from {restaurant.name} or look at other restaurants?",
                    'not_found': True,
                    'restaurant': restaurant.name,
                    'location': location
                }
    elif dish_name:
        return {
            'error': f"I couldn't find {restaurant_name} in {location}. Please check the restaurant name and location.",
            'restaurant_not_found': True
        }
    
    if not restaurant:
        return {
            'error': f"I couldn't find {restaurant_name}" + (f" in {location}" if location else "") + ". Please check the restaurant name and location.",
            'restaurant_not_found': True
        }
    
    if not menu_item:
        return {
            'error': "Please specify what dish you'd like to order.",
            'need_clarification': True
        }
    
    # Prepare order data
    delivery_address = user.address or "Address not set"
    phone = user.phone or "Phone not set"
    
    if delivery_address == "Address not set" or phone == "Phone not set":
        return {
            'error': "Please update your profile with delivery address and phone number before placing an order.",
            'need_profile_update': True
        }
    
    # Use payment method from intent or default to COD
    payment_method = order_intent.get('payment_method') or 'cash_on_delivery'
    
    # Create order items
    items = [{
        'menu_item_id': menu_item.id,
        'quantity': 1
    }]
    
    # Create the order
    order, error = OrderService.create_order(
        user_id=user_id,
        items=items,
        delivery_address=delivery_address,
        phone=phone,
        payment_method=payment_method,
        notes=f"AI Assistant order: {order_intent['original_message']}"
    )
    
    if error:
        return {'error': error}
    
    # Success response with friendly tone
    payment_text = "Cash on Delivery" if payment_method == 'cash_on_delivery' else payment_method.replace('_', ' ').title()
    
    return {
        'success': True,
        'message': f"Got it! 🍗 Ordering {menu_item.name} from {restaurant.name}, {location or restaurant.location} with {payment_text}. Your order has been placed!",
        'order': order.to_dict(),
        'order_details': {
            'dish': menu_item.name,
            'restaurant': restaurant.name,
            'location': location or restaurant.location,
            'price': menu_item.price,
            'payment_method': payment_method,
            'delivery_address': delivery_address
        }
    }


def generate_ai_response(message):
    """Generate AI response based on user message - Friendly and conversational tone"""
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'hola']):
        return "Hey! 👋 I'm your food assistant. Tell me what you're craving and where you want it from, and I'll get it sorted!"
    
    # Help requests
    elif any(word in message_lower for word in ['help', 'how to order', 'how do i']):
        return "Just tell me what you want! For example: 'Hot & Crispy Chicken from KFC Coimbatore' or 'Pizza from Dominos with cash on delivery'. I'll handle the rest! 🍕"
    
    # General food queries - Don't suggest random things
    elif any(word in message_lower for word in ['what should i', 'suggest', 'recommend']):
        return "I don't suggest random dishes, but if you tell me what you're in the mood for and where you want it from, I can help you order it! What are you craving? 🤔"
    
    # Asking about restaurants
    elif 'restaurant' in message_lower or 'hotels' in message_lower:
        return "Which restaurant are you thinking of? Tell me the name and what dish you want, and I'll check if it's available!"
    
    # Location queries
    elif any(word in message_lower for word in ['where', 'location', 'near me']):
        return "Just mention the area/location with the restaurant name when ordering. Like: 'Biryani from Paradise Coimbatore'. What would you like?"
    
    # Payment queries
    elif 'payment' in message_lower or 'pay' in message_lower or 'cod' in message_lower:
        return "I support cash on delivery, card, and online payment. Just mention your preference when ordering, like 'with cash on delivery' or 'with card'."
    
    # Generic food mentions without complete order info
    elif any(food in message_lower for food in ['biryani', 'pizza', 'burger', 'chicken', 'dosa', 'idli']):
        return "Sounds delicious! Which restaurant do you want it from? And which area? For example: 'Chicken Biryani from Paradise Coimbatore'"
    
    # Default friendly response
    else:
        return "Just tell me what dish you want, from which restaurant, and the location - I'll take care of it! You can also add 'with cash on delivery' if you prefer COD. 😊"
