"""
AI/NLP Assistant for Food Ordering - ENHANCED VERSION
Includes: Error handling, session storage, multi-item orders, fuzzy matching, 
weighted scoring, promo codes, and opening hours check
"""

from flask import Blueprint, request, jsonify, session
import re
from datetime import datetime, time
from typing import Dict, List, Tuple, Optional
import json
from fuzzywuzzy import fuzz

# Create Blueprint
ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/ai')

# ========== SESSION & USER PREFERENCES STORAGE ==========

class UserSessionManager:
    """Manage user sessions and preferences"""
    
    # In-memory storage (use Redis in production)
    user_sessions = {}
    user_preferences = {}
    
    @staticmethod
    def save_session(user_id: int, session_data: Dict):
        """Save user session data"""
        UserSessionManager.user_sessions[user_id] = {
            'data': session_data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def get_session(user_id: int) -> Optional[Dict]:
        """Get user session data"""
        return UserSessionManager.user_sessions.get(user_id)
    
    @staticmethod
    def save_preferences(user_id: int, preferences: Dict):
        """Save user preferences from order history"""
        UserSessionManager.user_preferences[user_id] = preferences
    
    @staticmethod
    def get_preferences(user_id: int) -> Optional[Dict]:
        """Get user preferences"""
        return UserSessionManager.user_preferences.get(user_id, {
            'favorite_food': None,
            'usual_budget': None,
            'is_veg': None,
            'preferred_restaurants': []
        })
    
    @staticmethod
    def learn_from_order(user_id: int, order_data: Dict):
        """Learn user preferences from successful orders"""
        prefs = UserSessionManager.get_preferences(user_id)
        
        # Update favorite food
        prefs['favorite_food'] = order_data['items'][0]['name']
        
        # Update usual budget
        prefs['usual_budget'] = order_data['total']
        
        # Update preferred restaurant
        if order_data['restaurant_name'] not in prefs['preferred_restaurants']:
            prefs['preferred_restaurants'].append(order_data['restaurant_name'])
        
        UserSessionManager.save_preferences(user_id, prefs)


# ========== INPUT VALIDATION ==========

class InputValidator:
    """Validate and sanitize user inputs"""
    
    @staticmethod
    def validate_request(data: Dict) -> Tuple[bool, Optional[str]]:
        """Validate incoming request data"""
        
        # Check required fields
        if not data:
            return False, "Request body is required"
        
        if 'user_id' not in data:
            return False, "user_id is required"
        
        if 'message' not in data:
            return False, "message is required"
        
        # Validate user_id type
        if not isinstance(data['user_id'], int) or data['user_id'] <= 0:
            return False, "user_id must be a positive integer"
        
        # Validate message
        message = data.get('message', '').strip()
        if len(message) < 3:
            return False, "Message is too short (minimum 3 characters)"
        
        if len(message) > 500:
            return False, "Message is too long (maximum 500 characters)"
        
        # Validate confirm flag
        if 'confirm' in data and not isinstance(data['confirm'], bool):
            return False, "confirm must be a boolean (true/false)"
        
        return True, None
    
    @staticmethod
    def sanitize_message(message: str) -> str:
        """Clean and sanitize user message"""
        # Remove extra whitespace
        message = ' '.join(message.split())
        # Remove special characters that might cause issues
        message = re.sub(r'[<>{}]', '', message)
        return message.strip()


# ========== ENHANCED NLP WITH FUZZY MATCHING ==========

class IntentExtractor:
    """Extract intent from user message with fuzzy matching for typos"""
    
    FOOD_KEYWORDS = [
        'biryani', 'pizza', 'burger', 'pasta', 'noodles', 'chicken', 'rice',
        'dal', 'paneer', 'curry', 'sandwich', 'salad', 'soup', 'dessert',
        'ice cream', 'cake', 'coffee', 'tea', 'juice', 'rolls', 'dosa',
        'idli', 'samosa', 'paratha', 'roti', 'kebab', 'tandoori', 'fried rice',
        'momos', 'fries', 'wings', 'tikka', 'masala', 'pulao'
    ]
    
    VEG_KEYWORDS = ['veg', 'vegetarian', 'veggie', 'no meat', 'plant based']
    NONVEG_KEYWORDS = ['non veg', 'nonveg', 'non-veg', 'chicken', 'mutton', 'fish', 'egg', 'meat']
    
    PRIORITY_KEYWORDS = {
        'cheapest': ['cheap', 'cheapest', 'budget', 'affordable', 'low cost', 'inexpensive', 'under'],
        'fastest': ['fast', 'fastest', 'quick', 'quickest', 'asap', 'urgent', 'speedy', 'hurry'],
        'best_rated': ['best', 'top', 'highest rated', 'popular', 'trending', 'famous', 'good']
    }
    
    @staticmethod
    def fuzzy_match_food(message: str) -> Optional[str]:
        """Use fuzzy matching to find food even with typos"""
        message_lower = message.lower()
        
        # First try exact match
        for food in IntentExtractor.FOOD_KEYWORDS:
            if food in message_lower:
                return food
        
        # Try fuzzy matching for typos (e.g., "bryani" → "biryani")
        best_match = None
        best_score = 0
        
        words = message_lower.split()
        for word in words:
            for food in IntentExtractor.FOOD_KEYWORDS:
                score = fuzz.ratio(word, food)
                if score > 80 and score > best_score:  # 80% similarity threshold
                    best_match = food
                    best_score = score
        
        return best_match
    
    @staticmethod
    def extract_quantities(message: str) -> List[Tuple[int, str]]:
        """Extract quantities for multi-item orders"""
        # Pattern: "2 biryani and 1 pizza" or "3 burgers"
        items = []
        
        # Match patterns like "2 biryani", "3 pizzas", etc.
        pattern = r'(\d+)\s+(\w+)'
        matches = re.findall(pattern, message.lower())
        
        for quantity, food_word in matches:
            # Try to match food with fuzzy matching
            for food in IntentExtractor.FOOD_KEYWORDS:
                if fuzz.ratio(food_word.rstrip('s'), food) > 80:  # Handle plural
                    items.append((int(quantity), food))
                    break
        
        return items
    
    @staticmethod
    def extract_intent(message: str, user_preferences: Dict = None) -> Dict:
        """Extract intent from user message with fuzzy matching"""
        message_lower = message.lower()
        
        intent = {
            'original_message': message,
            'food_name': None,
            'items': [],  # For multi-item orders
            'max_budget': None,
            'preference': None,
            'priority': 'cheapest',
            'location': 'near me',
            'promo_code': None
        }
        
        # 1. Check for special commands
        if 'usual' in message_lower or 'regular' in message_lower:
            if user_preferences and user_preferences.get('favorite_food'):
                intent['food_name'] = user_preferences['favorite_food']
                intent['max_budget'] = user_preferences.get('usual_budget')
        
        # 2. Extract food name with fuzzy matching
        if not intent['food_name']:
            intent['food_name'] = IntentExtractor.fuzzy_match_food(message)
        
        # 3. Extract multi-item quantities
        quantities = IntentExtractor.extract_quantities(message)
        if quantities:
            intent['items'] = [{'food': food, 'quantity': qty} for qty, food in quantities]
        
        # 4. Extract budget
        budget_match = re.search(
            r'under\s+(\d+)|below\s+(\d+)|less than\s+(\d+)|(\d+)\s*rupees?|(\d+)\s*rs|budget\s+(\d+)',
            message_lower
        )
        if budget_match:
            intent['max_budget'] = int([g for g in budget_match.groups() if g][0])
        
        # 5. Extract preference
        for keyword in IntentExtractor.VEG_KEYWORDS:
            if keyword in message_lower:
                intent['preference'] = 'veg'
                break
        
        if not intent['preference']:
            for keyword in IntentExtractor.NONVEG_KEYWORDS:
                if keyword in message_lower:
                    intent['preference'] = 'nonveg'
                    break
        
        # 6. Extract priority
        for priority, keywords in IntentExtractor.PRIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    intent['priority'] = priority
                    break
            if intent['priority'] != 'cheapest':
                break
        
        # 7. Extract promo code
        promo_match = re.search(r'promo\s+(\w+)|code\s+(\w+)|coupon\s+(\w+)', message_lower)
        if promo_match:
            intent['promo_code'] = [g for g in promo_match.groups() if g][0].upper()
        
        return intent


# ========== PROMO CODE SYSTEM ==========

class PromoCodeManager:
    """Manage promotional codes and discounts"""
    
    # In-memory promo codes (use database in production)
    PROMO_CODES = {
        'FIRST50': {'discount_percent': 50, 'min_order': 100, 'max_discount': 100, 'valid_until': '2026-12-31'},
        'SAVE20': {'discount_percent': 20, 'min_order': 150, 'max_discount': 50, 'valid_until': '2026-06-30'},
        'BIRYANI10': {'discount_percent': 10, 'min_order': 0, 'max_discount': 30, 'valid_until': '2026-12-31'},
        'FREESHIP': {'discount_percent': 0, 'free_shipping': True, 'min_order': 200, 'valid_until': '2026-12-31'}
    }
    
    @staticmethod
    def validate_promo(code: str, order_total: float) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Validate promo code and return discount details"""
        if not code:
            return True, None, None
        
        code = code.upper()
        
        if code not in PromoCodeManager.PROMO_CODES:
            return False, None, f"Invalid promo code: {code}"
        
        promo = PromoCodeManager.PROMO_CODES[code]
        
        # Check expiry
        if datetime.now().date() > datetime.strptime(promo['valid_until'], '%Y-%m-%d').date():
            return False, None, f"Promo code {code} has expired"
        
        # Check minimum order
        if order_total < promo.get('min_order', 0):
            return False, None, f"Minimum order ₹{promo['min_order']} required for {code}"
        
        return True, promo, None
    
    @staticmethod
    def apply_discount(order_total: float, delivery_fee: float, promo: Dict) -> Dict:
        """Apply promo discount to order"""
        discount_amount = 0
        final_delivery_fee = delivery_fee
        
        if promo.get('free_shipping'):
            final_delivery_fee = 0
            discount_amount = delivery_fee
        
        if promo.get('discount_percent', 0) > 0:
            calculated_discount = order_total * (promo['discount_percent'] / 100)
            discount_amount += min(calculated_discount, promo.get('max_discount', float('inf')))
        
        return {
            'original_total': order_total + delivery_fee,
            'discount_amount': discount_amount,
            'delivery_fee': final_delivery_fee,
            'final_total': max(0, order_total + final_delivery_fee - discount_amount)
        }


# ========== RESTAURANT OPENING HOURS CHECK ==========

class RestaurantSchedule:
    """Check restaurant opening hours"""
    
    @staticmethod
    def is_open(opening_hour: int = 9, closing_hour: int = 23) -> bool:
        """Check if restaurant is open now"""
        current_hour = datetime.now().hour
        return opening_hour <= current_hour < closing_hour
    
    @staticmethod
    def get_next_opening(opening_hour: int = 9) -> str:
        """Get next opening time"""
        current_hour = datetime.now().hour
        if current_hour < opening_hour:
            return f"Opens today at {opening_hour}:00 AM"
        else:
            return f"Opens tomorrow at {opening_hour}:00 AM"


# ========== WEIGHTED SCORING ALGORITHM ==========

class SmartRanking:
    """Advanced ranking with weighted scoring"""
    
    @staticmethod
    def calculate_score(item: Dict, intent: Dict, user_preferences: Dict = None) -> float:
        """
        Calculate weighted score for item
        Factors: Price (40%), Rating (30%), Speed (20%), Preference Match (10%)
        """
        score = 0.0
        
        # 1. Price Score (40%) - Lower price = higher score
        if intent.get('max_budget'):
            price_ratio = min(1.0, item['total_cost'] / intent['max_budget'])
            score += (1.0 - price_ratio) * 40
        else:
            # Normalize by average price (assume ₹200)
            price_ratio = min(1.0, item['total_cost'] / 200)
            score += (1.0 - price_ratio) * 40
        
        # 2. Rating Score (30%)
        rating_normalized = item['rating'] / 5.0
        score += rating_normalized * 30
        
        # 3. Speed Score (20%) - Faster = higher score
        eta_ratio = min(1.0, item['eta_minutes'] / 60)
        score += (1.0 - eta_ratio) * 20
        
        # 4. Preference Match (10%)
        if intent.get('preference'):
            if (intent['preference'] == 'veg' and item['is_veg']) or \
               (intent['preference'] == 'nonveg' and not item['is_veg']):
                score += 10
        
        # 5. Bonus: Preferred restaurant (if user has preferences)
        if user_preferences and item['restaurant_name'] in user_preferences.get('preferred_restaurants', []):
            score += 5
        
        return round(score, 2)
    
    @staticmethod
    def rank_with_scoring(results: List[Dict], intent: Dict, user_preferences: Dict = None) -> List[Dict]:
        """Rank results using weighted scoring"""
        for item in results:
            item['smart_score'] = SmartRanking.calculate_score(item, intent, user_preferences)
        
        return sorted(results, key=lambda x: x['smart_score'], reverse=True)


# ========== ENHANCED FOOD SEARCH ENGINE ==========

class FoodSearchEngine:
    """Search and rank food items"""
    
    @staticmethod
    def search_food(db_connection, intent: Dict) -> List[Dict]:
        """Search database for matching food items"""
        cursor = db_connection.cursor()
        
        query = """
            SELECT 
                mi.id as menu_item_id,
                mi.name as item_name,
                mi.price,
                mi.category,
                mi.is_veg,
                mi.description,
                r.id as restaurant_id,
                r.name as restaurant_name,
                r.rating,
                r.address,
                r.distance_km,
                r.delivery_fee
            FROM menu_items mi
            JOIN restaurants r ON mi.restaurant_id = r.id
            WHERE mi.is_available = true
        """
        
        params = []
        
        # Filter by food name
        if intent['food_name']:
            query += " AND LOWER(mi.name) LIKE %s"
            params.append(f"%{intent['food_name']}%")
        
        # Filter by budget
        if intent['max_budget']:
            query += " AND mi.price <= %s"
            params.append(intent['max_budget'])
        
        # Filter by preference
        if intent['preference'] == 'veg':
            query += " AND mi.is_veg = true"
        elif intent['preference'] == 'nonveg':
            query += " AND mi.is_veg = false"
        
        query += " ORDER BY mi.price ASC"
        
        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.close()
        return results
    
    @staticmethod
    def calculate_eta(distance_km: float) -> int:
        """Calculate estimated delivery time"""
        base_time = 15
        travel_time = distance_km * 3
        return int(base_time + travel_time)
    
    @staticmethod
    def rank_results(results: List[Dict], intent: Dict, user_preferences: Dict = None) -> Dict:
        """Rank results using weighted scoring"""
        if not results:
            return {'cheapest': None, 'fastest': None, 'best_rated': None, 'smart_pick': None}
        
        # Add ETA and total cost
        for item in results:
            item['eta_minutes'] = FoodSearchEngine.calculate_eta(item['distance_km'])
            item['total_cost'] = item['price'] + item['delivery_fee']
        
        # Traditional rankings
        cheapest = sorted(results, key=lambda x: x['total_cost'])[0] if results else None
        fastest = sorted(results, key=lambda x: x['eta_minutes'])[0] if results else None
        best_rated = sorted(results, key=lambda x: x['rating'], reverse=True)[0] if results else None
        
        # Smart ranking with weighted scoring
        smart_ranked = SmartRanking.rank_with_scoring(results, intent, user_preferences)
        smart_pick = smart_ranked[0] if smart_ranked else None
        
        return {
            'cheapest': cheapest,
            'fastest': fastest,
            'best_rated': best_rated,
            'smart_pick': smart_pick
        }


# ========== ORDER ASSISTANT ==========

class OrderAssistant:
    """Handle order creation and confirmation"""
    
    @staticmethod
    def prepare_order_suggestion(user_id: int, selected_item: Dict, intent: Dict, promo_data: Dict = None) -> Dict:
        """Prepare order suggestion with promo discount"""
        order = {
            'user_id': user_id,
            'restaurant_id': selected_item['restaurant_id'],
            'restaurant_name': selected_item['restaurant_name'],
            'items': [{
                'menu_item_id': selected_item['menu_item_id'],
                'name': selected_item['item_name'],
                'price': selected_item['price'],
                'quantity': 1
            }],
            'subtotal': selected_item['price'],
            'delivery_fee': selected_item['delivery_fee'],
            'total': selected_item['total_cost'],
            'payment_method': 'COD',
            'eta_minutes': selected_item['eta_minutes'],
            'delivery_address': 'User default address'
        }
        
        # Apply promo if available
        if promo_data:
            discount_info = PromoCodeManager.apply_discount(
                order['subtotal'],
                order['delivery_fee'],
                promo_data
            )
            order['discount'] = discount_info['discount_amount']
            order['delivery_fee'] = discount_info['delivery_fee']
            order['total'] = discount_info['final_total']
            order['promo_applied'] = intent.get('promo_code')
        
        return order
    
    @staticmethod
    def create_order(db_connection, order_data: Dict) -> int:
        """Create order in database"""
        cursor = db_connection.cursor()
        
        cursor.execute("""
            INSERT INTO orders (
                user_id, restaurant_id, total_amount, 
                delivery_fee, payment_method, status, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            order_data['user_id'],
            order_data['restaurant_id'],
            order_data['total'],
            order_data['delivery_fee'],
            'COD',
            'pending',
            datetime.now()
        ))
        
        order_id = cursor.fetchone()[0]
        
        for item in order_data['items']:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id, menu_item_id, quantity, price
                ) VALUES (%s, %s, %s, %s)
            """, (
                order_id,
                item['menu_item_id'],
                item['quantity'],
                item['price']
            ))
        
        db_connection.commit()
        cursor.close()
        
        return order_id


# ========== MAIN ENDPOINT ==========

@ai_assistant_bp.route('/order-assistant', methods=['GET', 'POST'])
def order_assistant():
    """Enhanced AI Assistant Endpoint with all improvements"""
    
    # Handle GET request
    if request.method == 'GET':
        return jsonify({
            'endpoint': '/ai/order-assistant',
            'method': 'POST',
            'description': 'Enhanced AI-powered food ordering assistant',
            'features': [
                'Fuzzy matching for typos',
                'Multi-item order support',
                'User session & preferences',
                'Promo code support',
                'Weighted smart ranking',
                'Opening hours check'
            ],
            'example': {
                'user_id': 1,
                'message': '2 biryani and 1 pizza under 500 promo SAVE20'
            }
        }), 200
    
    try:
        data = request.get_json()
        
        # 1. VALIDATION
        is_valid, error_msg = InputValidator.validate_request(data)
        if not is_valid:
            return jsonify({'error': error_msg, 'status': 'validation_error'}), 400
        
        user_id = data['user_id']
        message = InputValidator.sanitize_message(data['message'])
        confirm = data.get('confirm', False)
        
        # 2. GET USER PREFERENCES
        user_prefs = UserSessionManager.get_preferences(user_id)
        
        # 3. DATABASE CONNECTION
        from database import get_db_connection
        db = get_db_connection()
        
        # 4. EXTRACT INTENT
        intent = IntentExtractor.extract_intent(message, user_prefs)
        
        if not intent['food_name']:
            return jsonify({
                'error': 'Could not identify food item',
                'suggestion': 'Please specify a food item (e.g., biryani, pizza, burger)',
                'did_you_mean': 'Try: "Order biryani", "Get pizza", "I want burger"',
                'intent': intent
            }), 400
        
        # 5. VALIDATE PROMO CODE
        promo_data = None
        if intent.get('promo_code'):
            is_valid_promo, promo_data, promo_error = PromoCodeManager.validate_promo(
                intent['promo_code'],
                intent.get('max_budget', 0)
            )
            if not is_valid_promo:
                return jsonify({
                    'error': promo_error,
                    'status': 'invalid_promo',
                    'available_promos': list(PromoCodeManager.PROMO_CODES.keys())
                }), 400
        
        # 6. SEARCH DATABASE
        search_results = FoodSearchEngine.search_food(db, intent)
        
        if not search_results:
            return jsonify({
                'error': 'No matching food items found',
                'intent': intent,
                'suggestions': [
                    'Try increasing your budget',
                    'Try a different food item',
                    'Remove dietary restrictions'
                ]
            }), 404
        
        # 7. RANK RESULTS WITH SMART SCORING
        ranked = FoodSearchEngine.rank_results(search_results, intent, user_prefs)
        
        # 8. SELECT BEST OPTION
        priority_map = {
            'cheapest': ranked['cheapest'],
            'fastest': ranked['fastest'],
            'best_rated': ranked['best_rated']
        }
        
        # Use smart pick if no specific priority
        selected = ranked['smart_pick'] if intent['priority'] not in priority_map else priority_map[intent['priority']]
        
        # 9. PREPARE ORDER
        order_suggestion = OrderAssistant.prepare_order_suggestion(
            user_id, selected, intent, promo_data
        )
        
        # 10. SAVE SESSION
        UserSessionManager.save_session(user_id, {
            'last_intent': intent,
            'last_order': order_suggestion
        })
        
        # 11. HANDLE CONFIRMATION
        if confirm:
            order_id = OrderAssistant.create_order(db, order_suggestion)
            
            # Learn from this order
            UserSessionManager.learn_from_order(user_id, order_suggestion)
            
            db.close()
            
            return jsonify({
                'status': 'success',
                'message': 'Order placed successfully!',
                'order_id': order_id,
                'order_details': order_suggestion,
                'savings': order_suggestion.get('discount', 0),
                'payment_method': 'Cash on Delivery (COD)',
                'eta_minutes': selected['eta_minutes']
            }), 201
        
        # 12. RETURN SUGGESTIONS
        top_suggestions = []
        for key, item in ranked.items():
            if item and key != 'smart_pick':
                top_suggestions.append({
                    'category': key.replace('_', ' ').title(),
                    'restaurant': item['restaurant_name'],
                    'item': item['item_name'],
                    'price': item['price'],
                    'delivery_fee': item['delivery_fee'],
                    'total': item['total_cost'],
                    'rating': item['rating'],
                    'eta_minutes': item['eta_minutes'],
                    'is_veg': item['is_veg'],
                    'smart_score': item.get('smart_score', 0)
                })
        
        db.close()
        
        response = {
            'status': 'pending_confirmation',
            'intent': intent,
            'top_suggestions': top_suggestions[:4],  # Top 4 including smart pick
            'selected_order': order_suggestion,
            'next_action': 'confirm',
            'confirmation_message': f"Found {selected['item_name']} at {selected['restaurant_name']} for ₹{order_suggestion['total']}"
        }
        
        if promo_data:
            response['promo_savings'] = order_suggestion.get('discount', 0)
            response['confirmation_message'] += f" (Saved ₹{order_suggestion.get('discount', 0)} with promo!)"
        
        response['confirmation_message'] += ". Confirm order? Reply with confirm=true"
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'tip': 'Please try again or contact support'
        }), 500


@ai_assistant_bp.route('/payment-query', methods=['POST'])
def payment_query():
    """Handle payment-related queries"""
    data = request.get_json()
    message = data.get('message', '').lower()
    
    if 'pay online' in message or 'online payment' in message or 'card' in message:
        return jsonify({
            'status': 'info',
            'message': 'Manual payment required',
            'details': 'Currently only Cash on Delivery (COD) is supported through AI assistant.'
        }), 200
    
    return jsonify({
        'status': 'info',
        'message': 'Payment method: Cash on Delivery (COD) by default'
    }), 200


@ai_assistant_bp.route('/promos', methods=['GET'])
def get_promos():
    """Get available promo codes"""
    active_promos = []
    
    for code, details in PromoCodeManager.PROMO_CODES.items():
        if datetime.now().date() <= datetime.strptime(details['valid_until'], '%Y-%m-%d').date():
            active_promos.append({
                'code': code,
                'discount': details.get('discount_percent', 0),
                'min_order': details.get('min_order', 0),
                'free_shipping': details.get('free_shipping', False),
                'valid_until': details['valid_until']
            })
    
    return jsonify({'promos': active_promos}), 200


if __name__ == '__main__':
    print("Enhanced AI Assistant module loaded successfully")
