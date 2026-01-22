"""Enhanced AI Assistant for Food Ordering - Integrated with Flask Backend"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Restaurant, MenuItem, Order, OrderItem, User
from app.extensions import db
import re
from datetime import datetime
from fuzzywuzzy import fuzz
from typing import Dict, List, Optional

ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/ai')

# ========== USER SESSION MANAGER ==========
class UserSessionManager:
    """Manage user sessions and preferences"""
    user_sessions = {}
    user_preferences = {}
    
    @staticmethod
    def save_session(user_id: int, session_data: Dict):
        UserSessionManager.user_sessions[user_id] = {
            'data': session_data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def get_session(user_id: int) -> Optional[Dict]:
        return UserSessionManager.user_sessions.get(user_id)
    
    @staticmethod
    def save_preferences(user_id: int, preferences: Dict):
        UserSessionManager.user_preferences[user_id] = preferences
    
    @staticmethod
    def get_preferences(user_id: int) -> Optional[Dict]:
        return UserSessionManager.user_preferences.get(user_id, {
            'favorite_cuisine': None,
            'usual_budget': None,
            'is_veg': None,
        })

# ========== INPUT VALIDATOR ==========
class InputValidator:
    @staticmethod
    def sanitize_message(message: str) -> str:
        message = ' '.join(message.split())
        message = re.sub(r'[<>{}]', '', message)
        return message.strip()

# ========== INTENT EXTRACTOR WITH FUZZY MATCHING ==========
class IntentExtractor:
    FOOD_KEYWORDS = [
        'biryani', 'pizza', 'burger', 'pasta', 'noodles', 'chicken', 'rice',
        'paneer', 'curry', 'sandwich', 'salad', 'dessert', 'dosa', 'idli',
        'samosa', 'paratha', 'momos', 'fries', 'tikka', 'masala', 'meals',
        'coffee', 'tea', 'cake', 'sweet', 'whopper', 'sub', 'puri'
    ]
    
    PRIORITY_KEYWORDS = {
        'cheapest': ['cheap', 'cheapest', 'budget', 'affordable', 'low cost', 'under'],
        'fastest': ['fast', 'fastest', 'quick', 'quickest', 'asap', 'urgent'],
        'best_rated': ['best', 'top', 'highest rated', 'popular', 'trending', 'good']
    }
    
    @staticmethod
    def fuzzy_match_food(message: str) -> Optional[str]:
        """Use fuzzy matching to find food items even with typos"""
        message_lower = message.lower()
        
        # Try exact match first
        for food in IntentExtractor.FOOD_KEYWORDS:
            if food in message_lower:
                return food
        
        # Try fuzzy matching
        best_match = None
        best_score = 0
        for word in message_lower.split():
            for food in IntentExtractor.FOOD_KEYWORDS:
                score = fuzz.ratio(word, food)
                if score > 80 and score > best_score:  # 80% similarity threshold
                    best_score = score
                    best_match = food
        
        return best_match
    
    @staticmethod
    def extract_quantity(message: str) -> int:
        """Extract quantity from message"""
        match = re.search(r'(\d+)\s*(x|pieces?|items?)?', message.lower())
        return int(match.group(1)) if match else 1
    
    @staticmethod
    def extract_budget(message: str) -> Optional[int]:
        """Extract budget from message"""
        patterns = [
            r'under\s+(\d+)',
            r'below\s+(\d+)',
            r'less\s+than\s+(\d+)',
            r'within\s+(\d+)',
            r'max\s+(\d+)',
            r'₹\s*(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return int(match.group(1))
        return None
    
    @staticmethod
    def detect_priority(message: str) -> str:
        """Detect user's priority (cheapest, fastest, best_rated)"""
        message_lower = message.lower()
        
        for priority, keywords in IntentExtractor.PRIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return priority
        
        return 'best_rated'  # Default
    
    @staticmethod
    def is_vegetarian_request(message: str) -> Optional[bool]:
        """Detect if user wants vegetarian food"""
        message_lower = message.lower()
        veg_keywords = ['veg', 'vegetarian', 'veggie', 'no meat']
        nonveg_keywords = ['non veg', 'nonveg', 'chicken', 'mutton', 'fish', 'meat']
        
        for keyword in veg_keywords:
            if keyword in message_lower:
                return True
        for keyword in nonveg_keywords:
            if keyword in message_lower:
                return False
        return None

# ========== SMART RECOMMENDER ==========
class SmartRecommender:
    @staticmethod
    def weighted_score(item_data: Dict, priority: str) -> float:
        """Calculate weighted score based on priority"""
        weights = {
            'cheapest': {'price': 0.7, 'delivery_time': 0.1, 'rating': 0.2},
            'fastest': {'price': 0.1, 'delivery_time': 0.7, 'rating': 0.2},
            'best_rated': {'price': 0.2, 'delivery_time': 0.2, 'rating': 0.6}
        }
        
        w = weights.get(priority, weights['best_rated'])
        
        # Normalize values (inverse for price and time, direct for rating)
        price_score = 1 / (item_data['price'] / 100 + 1)
        time_score = 1 / (item_data['delivery_time'] / 10 + 1)
        rating_score = item_data['rating'] / 5.0
        
        return (w['price'] * price_score + 
                w['delivery_time'] * time_score + 
                w['rating'] * rating_score)
    
    @staticmethod
    def find_matching_items(food_type: str, budget: Optional[int], is_veg: Optional[bool]):
        """Find menu items matching criteria"""
        query = db.session.query(MenuItem, Restaurant).join(Restaurant)
        
        # Filter by food type using fuzzy matching
        matching_items = []
        all_items = query.all()
        
        for item, restaurant in all_items:
            # Check if item name or description matches food type
            name_score = fuzz.partial_ratio(food_type.lower(), item.name.lower())
            desc_score = fuzz.partial_ratio(food_type.lower(), (item.description or '').lower())
            
            if name_score > 60 or desc_score > 60:
                matching_items.append((item, restaurant))
        
        # Apply filters
        filtered_items = []
        for item, restaurant in matching_items:
            if budget and item.price > budget:
                continue
            
            if is_veg is not None and item.is_vegetarian != is_veg:
                continue
            
            if not item.is_available:
                continue
            
            filtered_items.append((item, restaurant))
        
        return filtered_items
    
    @staticmethod
    def rank_suggestions(items_restaurants: List, priority: str) -> List[Dict]:
        """Rank suggestions based on priority"""
        suggestions = []
        
        for item, restaurant in items_restaurants:
            delivery_time = 30
            if restaurant.delivery_time:
                times = re.findall(r'\d+', restaurant.delivery_time)
                if times:
                    delivery_time = sum(map(int, times)) / len(times)
            
            item_data = {
                'item_id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'restaurant_id': restaurant.id,
                'restaurant_name': restaurant.name,
                'delivery_time': delivery_time,
                'rating': restaurant.rating,
                'cuisine_type': restaurant.cuisine_type,
                'is_vegetarian': item.is_vegetarian
            }
            
            item_data['score'] = SmartRecommender.weighted_score(item_data, priority)
            suggestions.append(item_data)
        
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        
        return suggestions[:5]

# ========== MAIN ROUTE ==========
@ai_assistant_bp.route('/order-assistant', methods=['POST'])
@jwt_required()
def order_assistant():
    """Enhanced AI Assistant Endpoint"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        message = InputValidator.sanitize_message(message)
        user_prefs = UserSessionManager.get_preferences(user_id)
        
        food_type = IntentExtractor.fuzzy_match_food(message)
        quantity = IntentExtractor.extract_quantity(message)
        budget = IntentExtractor.extract_budget(message)
        priority = IntentExtractor.detect_priority(message)
        is_veg = IntentExtractor.is_vegetarian_request(message)
        
        if not food_type:
            response_text = generate_general_response(message)
            return jsonify({
                'response': response_text,
                'suggestions': []
            }), 200
        
        matching_items = SmartRecommender.find_matching_items(food_type, budget, is_veg)
        
        if not matching_items:
            return jsonify({
                'response': f"Sorry, I couldn't find any {food_type} that matches your criteria. Try adjusting your budget or preferences!",
                'suggestions': []
            }), 200
        
        suggestions = SmartRecommender.rank_suggestions(matching_items, priority)
        
        response_text = f"Great! I found {len(suggestions)} {food_type} options for you"
        if budget:
            response_text += f" under ₹{budget}"
        if is_veg:
            response_text += " (vegetarian)"
        response_text += f". Showing you the {priority.replace('_', ' ')} options:"
        
        UserSessionManager.save_session(user_id, {
            'last_query': message,
            'suggestions': suggestions[:3],
            'priority': priority
        })
        
        return jsonify({
            'response': response_text,
            'suggestions': suggestions,
            'filters': {
                'food_type': food_type,
                'quantity': quantity,
                'budget': budget,
                'priority': priority,
                'is_vegetarian': is_veg
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

def generate_general_response(message: str) -> str:
    """Generate response for general queries"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['recommend', 'suggest', 'what']):
        return "I'd recommend trying our popular restaurants! Tell me what you're craving - pizza, biryani, burgers, South Indian food, or something else?"
    
    elif any(word in message_lower for word in ['help', 'how']):
        return "I can help you find the perfect meal! Just tell me what you want to eat, your budget (optional), and any preferences. For example: 'I want 2 biryanis under 500 rupees' or 'Show me the best vegetarian pizza'"
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI food assistant. What would you like to eat today? 🍕"
    
    elif 'restaurant' in message_lower:
        restaurants = Restaurant.query.limit(5).all()
        names = [r.name for r in restaurants]
        return f"We have amazing restaurants like {', '.join(names[:3])} and more! What type of food are you looking for?"
    
    else:
        return "I'm here to help you order food! Tell me what you're craving, and I'll find the best options for you. You can also specify your budget or dietary preferences!"

@ai_assistant_bp.route('/session', methods=['GET'])
@jwt_required()
def get_session():
    """Get user's current session"""
    user_id = get_jwt_identity()
    session_data = UserSessionManager.get_session(user_id)
    
    return jsonify({
        'session': session_data,
        'preferences': UserSessionManager.get_preferences(user_id)
    }), 200

@ai_assistant_bp.route('/preferences', methods=['POST'])
@jwt_required()
def save_preferences():
    """Save user preferences"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    UserSessionManager.save_preferences(user_id, {
        'favorite_cuisine': data.get('favorite_cuisine'),
        'usual_budget': data.get('usual_budget'),
        'is_veg': data.get('is_veg')
    })
    
    return jsonify({'message': 'Preferences saved successfully'}), 200
