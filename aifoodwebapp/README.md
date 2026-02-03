# AI Food Ordering Assistant

An intelligent NLP-powered food ordering system built with Flask and PostgreSQL.

## 🚀 Features

- **Natural Language Processing**: Users can order food using natural language
- **Smart Intent Extraction**: Automatically detects food name, budget, preferences, and priorities
- **Intelligent Ranking**: Returns top 3 options (cheapest, fastest, best-rated)
- **Auto Order Preparation**: Prepares order with Cash on Delivery by default
- **Simple Confirmation Flow**: Easy yes/no confirmation for orders

## 📋 API Endpoint

### POST `/ai/order-assistant`

**Input:**
```json
{
  "user_id": 1,
  "message": "Order cheapest biryani under 200 near me"
}
```

**Output:**
```json
{
  "status": "pending_confirmation",
  "intent": {
    "food_name": "biryani",
    "max_budget": 200,
    "preference": null,
    "priority": "cheapest"
  },
  "top3_suggestions": [
    {
      "category": "Cheapest",
      "restaurant": "Food Court Express",
      "item": "Mini Chicken Biryani",
      "price": 90,
      "delivery_fee": 40,
      "total": 130,
      "rating": 4.0,
      "eta_minutes": 28
    },
    ...
  ],
  "selected_order": {
    "restaurant_name": "Food Court Express",
    "items": [...],
    "total": 130,
    "payment_method": "COD"
  },
  "next_action": "confirm",
  "confirmation_message": "Found Mini Chicken Biryani..."
}
```

**Confirm Order:**
```json
{
  "user_id": 1,
  "message": "Order cheapest biryani under 200 near me",
  "confirm": true
}
```

## 🎯 AI Capabilities

### 1. Intent Extraction
- **Food Name**: Detects 30+ food items (biryani, pizza, burger, pasta, etc.)
- **Budget**: Extracts price limits (under 200, below 150, less than 300)
- **Preference**: Identifies veg/non-veg preferences
- **Priority**: Determines cheapest/fastest/best-rated

### 2. Database Search
- Matches restaurants and menu items
- Filters by budget, preference, availability
- Ranks by price, ETA, and rating

### 3. Smart Suggestions
Returns exactly 3 options:
1. **Cheapest**: Lowest total cost (item + delivery)
2. **Fastest**: Shortest estimated delivery time
3. **Best Rated**: Highest restaurant rating

### 4. Order Automation
- Auto-selects best option based on user priority
- Prepares complete order with COD
- Single confirmation step

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database
python database.py

# Run server
python app.py
```

## 🧪 Testing

```bash
# Run unit tests
python test_ai_assistant.py

# Test with curl
curl -X POST http://localhost:5000/ai/order-assistant \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "Order cheapest biryani under 200 near me"
  }'
```

## 📝 Example Messages

```
"Order cheapest biryani under 200 near me"
"I want fastest veg pizza delivery"
"Show me best chicken biryani under 150 rupees"
"Get me cheap vegetarian biryani below 180"
"Order chicken biryani asap"
"I want the most popular pizza"
```

## 💳 Payment

- **Default**: Cash on Delivery (COD)
- **Online Payment**: Returns "Manual payment required" message

## 🗄️ Database Schema

### restaurants
- id, name, address, rating, distance_km, delivery_fee

### menu_items
- id, restaurant_id, name, price, category, is_veg, is_available

### orders
- id, user_id, restaurant_id, total_amount, payment_method, status

### order_items
- id, order_id, menu_item_id, quantity, price

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **NLP**: Regex-based intent extraction
- **Architecture**: Blueprint-based modular design

## 📊 Features Implemented

✅ NLP Intent Extraction (food, budget, preference, priority)  
✅ PostgreSQL database queries with filtering  
✅ Top 3 ranking (cheapest, fastest, best-rated)  
✅ Auto order preparation with COD  
✅ Confirmation flow  
✅ Payment query handling  
✅ Sample data seeding  
✅ Test cases with CURL examples  

## 🚦 API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /ai/order-assistant` - Main AI assistant
- `POST /ai/payment-query` - Payment queries

## 👨‍💻 Development

This module is designed to work independently. Your team members can integrate:
- **Frontend**: Call the API endpoints
- **Backend**: Import `ai_assistant_bp` blueprint
- **Database**: Use existing schema or modify as needed

## 📄 License

This is a team project module developed by Kavin.
