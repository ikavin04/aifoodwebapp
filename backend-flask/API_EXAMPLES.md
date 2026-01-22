# API Testing Examples

## Base URL
```
http://localhost:5000
```

---

## 1. Health Check

### Check API Status
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 2. Authentication

### Register New User
```bash
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "1234567890",
  "address": "123 Main St, City"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St, City"
  }
}
```

### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Get Current User
```bash
GET /auth/me
Authorization: Bearer <access_token>
```

---

## 3. Restaurants

### Get All Restaurants
```bash
GET /restaurants
```

**Response (200):**
```json
{
  "restaurants": [
    {
      "id": 1,
      "name": "Pizza Palace",
      "description": "Authentic Italian pizzas",
      "cuisine_type": "Italian",
      "rating": 4.5,
      "delivery_time": "30-40 mins"
    }
  ],
  "count": 5
}
```

### Search Restaurants
```bash
GET /restaurants?query=pizza
GET /restaurants?cuisine_type=Italian
GET /restaurants?query=burger&cuisine_type=American
```

### Get Restaurant by ID
```bash
GET /restaurants/1
```

### Get Restaurant Menu
```bash
GET /restaurants/1/menu
```

**Response (200):**
```json
{
  "menu_items": [
    {
      "id": 1,
      "restaurant_id": 1,
      "name": "Margherita Pizza",
      "description": "Classic tomato, mozzarella, and basil",
      "price": 12.99,
      "category": "Pizza",
      "is_vegetarian": true,
      "is_available": true
    }
  ],
  "count": 5
}
```

---

## 4. Cart (Protected)

**Note:** All cart endpoints require `Authorization: Bearer <access_token>` header

### Add Item to Cart
```bash
POST /cart/add
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "menu_item_id": 1,
  "quantity": 2
}
```

**Response (201):**
```json
{
  "message": "Item added to cart",
  "cart_item": {
    "id": 1,
    "menu_item_id": 1,
    "quantity": 2,
    "subtotal": 25.98
  }
}
```

### Get Cart
```bash
GET /cart
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "cart_items": [
    {
      "id": 1,
      "menu_item": {
        "id": 1,
        "name": "Margherita Pizza",
        "price": 12.99
      },
      "quantity": 2,
      "subtotal": 25.98
    }
  ],
  "total": 25.98,
  "count": 1
}
```

### Update Cart Item
```bash
PUT /cart/update/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quantity": 3
}
```

### Remove Item from Cart
```bash
DELETE /cart/remove/1
Authorization: Bearer <access_token>
```

### Clear Cart
```bash
DELETE /cart/clear
Authorization: Bearer <access_token>
```

---

## 5. Orders (Protected)

**Note:** All order endpoints require `Authorization: Bearer <access_token>` header

### Place Order
```bash
POST /orders
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    },
    {
      "menu_item_id": 2,
      "quantity": 1
    }
  ],
  "delivery_address": "123 Main St, City",
  "phone": "1234567890",
  "notes": "Please ring doorbell"
}
```

**Response (201):**
```json
{
  "message": "Order placed successfully",
  "order": {
    "id": 1,
    "restaurant_id": 1,
    "restaurant_name": "Pizza Palace",
    "total_amount": 40.97,
    "status": "pending",
    "payment_method": "cash_on_delivery",
    "delivery_address": "123 Main St, City",
    "phone": "1234567890",
    "items": [
      {
        "menu_item_name": "Margherita Pizza",
        "quantity": 2,
        "price": 12.99,
        "subtotal": 25.98
      }
    ]
  }
}
```

### Get Order History
```bash
GET /orders/history
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "orders": [
    {
      "id": 1,
      "restaurant_name": "Pizza Palace",
      "total_amount": 40.97,
      "status": "delivered",
      "created_at": "2026-01-22T10:30:00"
    }
  ],
  "count": 3
}
```

### Get Order Details
```bash
GET /orders/1
Authorization: Bearer <access_token>
```

### Cancel Order
```bash
PUT /orders/1/cancel
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Order cancelled successfully",
  "order": {
    "id": 1,
    "status": "cancelled"
  }
}
```

### Update Order Status (Admin)
```bash
PUT /orders/1/status
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "confirmed"
}
```

**Valid Status Values:**
- `pending`
- `confirmed`
- `preparing`
- `out_for_delivery`
- `delivered`
- `cancelled`

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": ["Email is required", "Password must be at least 6 characters"]
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid email or password"
}
```

### 404 Not Found
```json
{
  "error": "Restaurant not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "Error message"
}
```

---

## cURL Examples

### Register
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@test.com","password":"test123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@test.com","password":"test123"}'
```

### Get Restaurants
```bash
curl http://localhost:5000/restaurants
```

### Add to Cart (with token)
```bash
curl -X POST http://localhost:5000/cart/add \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"menu_item_id":1,"quantity":2}'
```

### Place Order (with token)
```bash
curl -X POST http://localhost:5000/orders \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"menu_item_id":1,"quantity":2}],"delivery_address":"123 Main St","phone":"1234567890"}'
```

---

## PowerShell Examples

### Register
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/auth/register" -Method Post -ContentType "application/json" -Body '{"name":"John Doe","email":"john@test.com","password":"test123"}'
```

### Login
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"john@test.com","password":"test123"}'
$token = $response.access_token
```

### Get Restaurants
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/restaurants"
```

### Add to Cart
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}
Invoke-RestMethod -Uri "http://localhost:5000/cart/add" -Method Post -Headers $headers -Body '{"menu_item_id":1,"quantity":2}'
```
