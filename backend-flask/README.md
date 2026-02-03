# Food Ordering Backend - Flask REST API

A complete Flask backend for a food ordering application with JWT authentication, PostgreSQL database, and RESTful APIs.

## 🚀 Features

- ✅ User authentication (register/login) with JWT
- ✅ Restaurant management
- ✅ Menu item browsing
- ✅ Shopping cart functionality
- ✅ Order placement and tracking
- ✅ Order history
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive error handling
- ✅ Sample data seeding

## 📦 Tech Stack

- **Python 3.8+**
- **Flask** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - Authentication
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - CORS support

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- pip (Python package manager)

### Setup Steps

1. **Navigate to backend directory**
   ```bash
   cd backend-flask
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update database credentials and secret keys
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/foodorder_db
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   ```

6. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE foodorder_db;
   ```

7. **Initialize database migrations**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. **Seed sample data**
   ```bash
   python seed.py
   ```

9. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "1234567890",
  "address": "123 Main St"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

### Restaurants

#### Get All Restaurants
```http
GET /restaurants
```

#### Search Restaurants
```http
GET /restaurants?query=pizza&cuisine_type=Italian
```

#### Get Restaurant Details
```http
GET /restaurants/{restaurant_id}
```

#### Get Restaurant Menu
```http
GET /restaurants/{restaurant_id}/menu
```

### Cart (Protected Routes)

#### Get Cart
```http
GET /cart
Authorization: Bearer <access_token>
```

#### Add to Cart
```http
POST /cart/add
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "menu_item_id": 1,
  "quantity": 2
}
```

#### Update Cart Item
```http
PUT /cart/update/{item_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quantity": 3
}
```

#### Remove from Cart
```http
DELETE /cart/remove/{item_id}
Authorization: Bearer <access_token>
```

#### Clear Cart
```http
DELETE /cart/clear
Authorization: Bearer <access_token>
```

### Orders (Protected Routes)

#### Place Order
```http
POST /orders
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    }
  ],
  "delivery_address": "123 Main St, City",
  "phone": "1234567890",
  "notes": "Please ring the doorbell"
}
```

#### Get Order History
```http
GET /orders/history
Authorization: Bearer <access_token>
```

#### Get Order Details
```http
GET /orders/{order_id}
Authorization: Bearer <access_token>
```

#### Cancel Order
```http
PUT /orders/{order_id}/cancel
Authorization: Bearer <access_token>
```

#### Update Order Status (Admin)
```http
PUT /orders/{order_id}/status
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "confirmed"
}
```

Status values: `pending`, `confirmed`, `preparing`, `out_for_delivery`, `delivered`, `cancelled`

## 🗂️ Project Structure

```
backend-flask/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration settings
│   ├── extensions.py         # Flask extensions
│   ├── models/
│   │   └── __init__.py       # Database models
│   ├── routes/
│   │   ├── auth.py           # Authentication routes
│   │   ├── restaurant.py     # Restaurant routes
│   │   ├── cart.py           # Cart routes
│   │   └── order.py          # Order routes
│   ├── services/
│   │   ├── auth_service.py   # Auth business logic
│   │   ├── restaurant_service.py
│   │   ├── cart_service.py
│   │   └── order_service.py
│   └── utils/
│       └── validators.py     # Input validation
├── migrations/               # Database migrations
├── seed.py                   # Sample data seeding
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔐 Test Credentials

After seeding the database, you can use:
- **Email:** test@example.com
- **Password:** password123

## 🧪 Testing the API

You can test the API using:
- **Postman** - Import endpoints and test
- **cURL** - Command line testing
- **HTTPie** - User-friendly CLI tool

Example with cURL:
```bash
# Register
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Get restaurants
curl http://localhost:5000/restaurants
```

## 📝 Database Models

- **User** - User accounts with authentication
- **Restaurant** - Restaurant information
- **MenuItem** - Menu items belonging to restaurants
- **Order** - Customer orders
- **OrderItem** - Items in an order (many-to-many)
- **Cart** - Shopping cart items

## 🔄 Order Status Flow

```
pending → confirmed → preparing → out_for_delivery → delivered
         ↓
      cancelled
```

## 🛡️ Security Features

- Password hashing using Werkzeug
- JWT token-based authentication
- Protected routes with `@jwt_required()`
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy ORM

## 🚦 Error Handling

The API returns consistent JSON error responses:
```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

## 🤝 Integration with Frontend

This backend is designed to work with any frontend framework (React, Vue, Angular, etc.). Make sure to:

1. Set correct CORS origins in `.env`
2. Include JWT token in Authorization header for protected routes
3. Handle token expiration and refresh

## 📄 License

This project is part of a food ordering application with AI assistance.

## 👥 Team

Backend developed for a 3-person team project.
