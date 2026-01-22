# INTEGRATION GUIDE FOR TEAM

## 🤝 For Your Teammates

---

## 👨‍💻 Frontend Developer

### What You Need to Know:
The AI assistant provides a simple REST API endpoint that accepts natural language input.

### API Endpoint:
```
POST http://localhost:5000/ai/order-assistant
```

### Basic Integration Example:

```javascript
// Step 1: User types message
const userMessage = "Order cheapest biryani under 200 near me";

// Step 2: Send to AI API
async function askAI(message) {
  const response = await fetch('http://localhost:5000/ai/order-assistant', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: getCurrentUserId(), // Your user management
      message: message
    })
  });
  
  return await response.json();
}

// Step 3: Display suggestions
const result = await askAI(userMessage);

if (result.status === 'pending_confirmation') {
  // Show the 3 suggestions
  displaySuggestions(result.top3_suggestions);
  
  // Show the auto-selected order
  displaySelectedOrder(result.selected_order);
  
  // Show confirmation button
  showConfirmButton(() => confirmOrder(userMessage));
}

// Step 4: User confirms
async function confirmOrder(originalMessage) {
  const response = await fetch('http://localhost:5000/ai/order-assistant', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: getCurrentUserId(),
      message: originalMessage,
      confirm: true  // ← This triggers order creation
    })
  });
  
  const result = await response.json();
  
  if (result.status === 'success') {
    showOrderConfirmation(result.order_id);
  }
}
```

### UI Components Needed:
1. **Input Box**: For user to type natural language
2. **Suggestions Card**: Display top 3 options
3. **Selected Order Card**: Show auto-selected order
4. **Confirm Button**: To place order
5. **Success Message**: After order placed

### Sample Response Structure:
```json
{
  "status": "pending_confirmation",
  "top3_suggestions": [
    {
      "category": "Cheapest",
      "restaurant": "Food Court Express",
      "item": "Mini Chicken Biryani",
      "price": 90,
      "delivery_fee": 40,
      "total": 130,
      "rating": 4.0,
      "eta_minutes": 28,
      "is_veg": false
    }
  ],
  "selected_order": {
    "restaurant_name": "Food Court Express",
    "items": [{"name": "Mini Chicken Biryani", "price": 90}],
    "total": 130,
    "payment_method": "COD"
  }
}
```

---

## 🔧 Backend Developer

### What You Need to Know:
The AI assistant is a Flask Blueprint that can be imported into your main app.

### Integration Steps:

```python
# In your main app.py or __init__.py

from flask import Flask
from ai_assistant import ai_assistant_bp  # ← Import the blueprint

app = Flask(__name__)

# Register the AI blueprint
app.register_blueprint(ai_assistant_bp)  # ← This adds /ai/* routes

# Your existing routes
@app.route('/api/restaurants')
def get_restaurants():
    # Your code
    pass

if __name__ == '__main__':
    app.run()
```

### Available Routes:
- `POST /ai/order-assistant` - Main AI endpoint
- `POST /ai/payment-query` - Payment queries

### Database Connection:
The AI module uses `database.py` which expects:
```python
from database import get_db_connection

conn = get_db_connection()
# Uses environment variables from .env
```

### Environment Variables:
Make sure your `.env` has:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_ordering_db
DB_USER=postgres
DB_PASSWORD=postgres
```

### Error Handling:
The API returns proper HTTP status codes:
- `200` - Success with suggestions
- `201` - Order created successfully
- `400` - Bad request (missing fields)
- `404` - No results found
- `500` - Server error

---

## 🗄️ Database Developer

### Required Tables:

```sql
-- Table 1: Restaurants
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    rating DECIMAL(2,1) DEFAULT 0.0,
    distance_km DECIMAL(5,2) DEFAULT 0.0,
    delivery_fee DECIMAL(10,2) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Menu Items
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    is_veg BOOLEAN DEFAULT true,
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER REFERENCES restaurants(id),
    total_amount DECIMAL(10,2) NOT NULL,
    delivery_fee DECIMAL(10,2) DEFAULT 0.0,
    payment_method VARCHAR(50) DEFAULT 'COD',
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 4: Order Items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    menu_item_id INTEGER REFERENCES menu_items(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes for Performance:
```sql
CREATE INDEX idx_menu_items_name ON menu_items(name);
CREATE INDEX idx_menu_items_price ON menu_items(price);
CREATE INDEX idx_menu_items_restaurant ON menu_items(restaurant_id);
CREATE INDEX idx_restaurants_rating ON restaurants(rating);
CREATE INDEX idx_orders_user ON orders(user_id);
```

### Sample Data:
Run `python database.py` to create tables and insert sample data.

### Critical Fields:
- `menu_items.is_available` - Must be TRUE for AI to find items
- `menu_items.is_veg` - Used for veg/nonveg filtering
- `restaurants.distance_km` - Used for ETA calculation
- `restaurants.delivery_fee` - Added to total cost

---

## 🔄 Complete Integration Flow

```
┌─────────────┐
│   FRONTEND  │
│  (React/Vue)│
└──────┬──────┘
       │ User types: "Order cheapest biryani under 200"
       │
       ▼
┌─────────────┐
│   AI API    │  ← Kavin's Module
│ /ai/order-  │
│  assistant  │
└──────┬──────┘
       │ 1. Extract intent (food=biryani, budget=200, priority=cheapest)
       │ 2. Query database
       │
       ▼
┌─────────────┐
│  DATABASE   │  ← Database Team
│ PostgreSQL  │
└──────┬──────┘
       │ Returns: restaurants + menu_items
       │
       ▼
┌─────────────┐
│  RANKING    │  ← Kavin's Module
│  ENGINE     │
└──────┬──────┘
       │ Calculates: cheapest, fastest, best-rated
       │
       ▼
┌─────────────┐
│   RESPONSE  │
│  Top 3 +    │
│  Selected   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FRONTEND  │
│  Shows      │
│ suggestions │
└──────┬──────┘
       │ User clicks "Confirm"
       │
       ▼
┌─────────────┐
│   AI API    │
│ confirm=true│
└──────┬──────┘
       │ Creates order in database
       │
       ▼
┌─────────────┐
│  DATABASE   │
│ Orders +    │
│ OrderItems  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ ORDER CONF. │
│ order_id=1  │
└─────────────┘
```

---

## 🧪 Testing Together

### 1. Database Team Sets Up:
```bash
python database.py  # Creates tables + sample data
```

### 2. Backend Team Integrates:
```python
from ai_assistant import ai_assistant_bp
app.register_blueprint(ai_assistant_bp)
```

### 3. Start Server:
```bash
python app.py
```

### 4. Frontend Team Tests:
```bash
# Test endpoint is alive
curl http://localhost:5000/health

# Test AI assistant
curl -X POST http://localhost:5000/ai/order-assistant \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "message": "Order cheapest biryani under 200"}'
```

---

## 📝 Communication Protocol

### Frontend → Backend:
```json
{
  "user_id": 1,
  "message": "natural language string",
  "confirm": false/true
}
```

### Backend → Frontend:
```json
{
  "status": "pending_confirmation" | "success" | "error",
  "intent": {...},
  "top3_suggestions": [...],
  "selected_order": {...}
}
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "No module named 'ai_assistant'"
**Solution:** Make sure all files are in same directory

### Issue 2: Database connection error
**Solution:** Check `.env` file and PostgreSQL is running

### Issue 3: "No matching food items found"
**Solution:** Run `python database.py` to seed sample data

### Issue 4: CORS error in frontend
**Solution:** Backend team needs to enable CORS:
```python
from flask_cors import CORS
CORS(app)
```

---

## 📞 Need Help?

**Kavin (AI Module):** Questions about AI logic, intent extraction, ranking
**Database Team:** Questions about tables, queries, data
**Backend Team:** Questions about Flask, blueprints, integration
**Frontend Team:** Questions about API calls, UI components

---

## ✅ Integration Checklist

- [ ] Database: Tables created with correct schema
- [ ] Database: Sample data inserted
- [ ] Backend: Blueprint imported and registered
- [ ] Backend: .env configured
- [ ] Frontend: API endpoint integrated
- [ ] Frontend: UI components for suggestions built
- [ ] Frontend: Confirmation flow implemented
- [ ] Testing: End-to-end flow works
- [ ] Testing: All edge cases handled

---

## 🚀 Go Live Checklist

- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Error handling tested
- [ ] Database indexed for performance
- [ ] API documented
- [ ] Frontend UX reviewed
- [ ] Security review (SQL injection, etc.)
- [ ] Load testing completed

---

**Integration Status:** Ready ✅  
**Next Step:** Each team integrates their part  
**Target:** Complete integration by [DATE]
