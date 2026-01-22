"""AI Assistant routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/order-assistant', methods=['POST'])
@jwt_required()
def order_assistant():
    """AI order assistant endpoint"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        message = data.get('message', '')
        
        # Simple AI response logic (you can integrate with OpenAI/Claude later)
        response_message = generate_ai_response(message)
        
        return jsonify({
            'response': response_message,
            'suggestions': []
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


def generate_ai_response(message):
    """Generate AI response based on user message"""
    message_lower = message.lower()
    
    # Simple rule-based responses
    if 'recommend' in message_lower or 'suggest' in message_lower:
        return "I'd recommend trying our popular restaurants like Shree Annapoorna for authentic South Indian meals or Anjappar Chettinad for spicy Chettinad cuisine. What type of food are you in the mood for?"
    
    elif 'biryani' in message_lower:
        return "Great choice! I suggest Hotel Junior Kuppanna for their amazing Mutton Biryani or That's Y Food for Chicken Biryani. Both are highly rated!"
    
    elif 'vegetarian' in message_lower or 'veg' in message_lower:
        return "For pure vegetarian food, I highly recommend Shree Annapoorna or Haribhavanam. They serve delicious South Indian vegetarian meals!"
    
    elif 'pizza' in message_lower:
        return "Domino's Pizza has great options! Their Farmhouse Pizza and Margherita are customer favorites. Would you like me to help you place an order?"
    
    elif 'fast' in message_lower or 'quick' in message_lower:
        return "For quick delivery, try Geetha Cafe (20-30 mins), Subway (20-30 mins), or Burger King (25-35 mins). They're all nearby and fast!"
    
    elif 'cheap' in message_lower or 'budget' in message_lower:
        return "For budget-friendly options, check out Geetha Cafe for dosas and idlis, or Haribhavanam for affordable meals. Great taste at great prices!"
    
    elif 'spicy' in message_lower:
        return "If you love spicy food, Anjappar Chettinad is perfect for you! Their Chicken Chettinad and Crab Masala are super spicy and flavorful."
    
    elif 'sweet' in message_lower or 'dessert' in message_lower:
        return "Sree Anandhaas is the place for sweets! Try their famous Mysore Pak or Gulab Jamun. Domino's also has Choco Lava Cake if you want something different."
    
    elif 'order' in message_lower or 'help' in message_lower:
        return "I can help you place an order! Just browse the restaurants, add items to your cart, and proceed to checkout. Need recommendations?"
    
    else:
        return "I'm here to help you find the perfect meal! You can ask me for restaurant recommendations, check out our menu, or get help placing an order. What would you like to know?"
