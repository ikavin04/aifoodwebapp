# 🚀 Backend Setup Checklist

Use this checklist to get your Flask backend up and running!

## ✅ Pre-requisites

- [ ] Python 3.8+ installed
- [ ] PostgreSQL installed and running
- [ ] Git installed (for version control)
- [ ] Terminal/PowerShell access
- [ ] Code editor (VS Code recommended)

---

## 📦 Step 1: Environment Setup

- [ ] Navigate to backend-flask directory
  ```powershell
  cd "F:\Food order app AI\backend-flask"
  ```

- [ ] Create virtual environment
  ```powershell
  python -m venv venv
  ```

- [ ] Activate virtual environment
  ```powershell
  .\venv\Scripts\activate
  ```
  ✅ You should see `(venv)` in your terminal

- [ ] Install dependencies
  ```powershell
  pip install -r requirements.txt
  ```
  ⏱️ This will take 1-2 minutes

---

## 🗄️ Step 2: Database Setup

- [ ] Start PostgreSQL service
  - Windows: Check Services or pgAdmin
  - Run: `pg_isready` to verify

- [ ] Create database
  ```sql
  -- Option 1: Using psql
  psql -U postgres
  CREATE DATABASE foodorder_db;
  \q

  -- Option 2: Using pgAdmin
  Right-click Databases → Create → Database
  Name: foodorder_db
  ```

- [ ] Update `.env` file with your database credentials
  ```env
  DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/foodorder_db
  ```
  ⚠️ Replace `YOUR_PASSWORD` with your actual PostgreSQL password

- [ ] Update secret keys in `.env`
  ```env
  SECRET_KEY=your-secret-key-change-this
  JWT_SECRET_KEY=your-jwt-secret-change-this
  ```

---

## 🔄 Step 3: Database Migrations

- [ ] Set Flask app environment variable
  ```powershell
  $env:FLASK_APP="run.py"
  ```

- [ ] Initialize migrations
  ```powershell
  flask db init
  ```
  ✅ Creates `migrations/` folder

- [ ] Create initial migration
  ```powershell
  flask db migrate -m "Initial migration"
  ```
  ✅ Creates migration file in `migrations/versions/`

- [ ] Apply migrations to database
  ```powershell
  flask db upgrade
  ```
  ✅ Creates all tables in database

- [ ] Verify tables were created
  ```sql
  -- Using psql
  psql -U postgres -d foodorder_db
  \dt
  
  -- You should see: users, restaurants, menu_items, orders, order_items, cart
  ```

---

## 🌱 Step 4: Seed Sample Data

- [ ] Run seed script
  ```powershell
  python seed.py
  ```
  ✅ You should see:
  ```
  🌱 Starting database seeding...
  👥 Creating sample users...
  ✅ Created 3 users
  🍽️ Creating sample restaurants...
  ✅ Created 5 restaurants
  📝 Creating menu items...
  ✅ Created 25 menu items
  ✨ Database seeding completed successfully!
  ```

- [ ] Verify data was inserted
  ```sql
  -- Check users
  SELECT COUNT(*) FROM users;  -- Should be 3
  
  -- Check restaurants
  SELECT COUNT(*) FROM restaurants;  -- Should be 5
  
  -- Check menu items
  SELECT COUNT(*) FROM menu_items;  -- Should be 25
  ```

---

## 🏃 Step 5: Run the Application

- [ ] Start Flask server
  ```powershell
  python run.py
  ```
  ✅ You should see:
  ```
  * Running on http://0.0.0.0:5000
  * Debug mode: on
  ```

- [ ] Test health endpoint in browser
  - Open: http://localhost:5000/health
  - Should see: `{"status":"healthy"}`

- [ ] Test API info endpoint
  - Open: http://localhost:5000/
  - Should see API information

---

## 🧪 Step 6: Test API Endpoints

### Test 1: Get Restaurants (Public)
- [ ] Test in browser or run:
  ```powershell
  curl http://localhost:5000/restaurants
  ```
  ✅ Should return list of 5 restaurants

### Test 2: Register User
- [ ] Register a new user:
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:5000/auth/register" -Method Post -ContentType "application/json" -Body '{"name":"Test User","email":"mytest@test.com","password":"test123"}'
  ```
  ✅ Should return success message and user data

### Test 3: Login
- [ ] Login with test user:
  ```powershell
  $response = Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -ContentType "application/json" -Body '{"email":"test@example.com","password":"password123"}'
  $token = $response.access_token
  Write-Host "Token: $token"
  ```
  ✅ Should return access token

### Test 4: Get Current User (Protected)
- [ ] Get user info with token:
  ```powershell
  $headers = @{"Authorization" = "Bearer $token"}
  Invoke-RestMethod -Uri "http://localhost:5000/auth/me" -Headers $headers
  ```
  ✅ Should return user data

### Test 5: Add to Cart (Protected)
- [ ] Add item to cart:
  ```powershell
  $headers = @{
      "Authorization" = "Bearer $token"
      "Content-Type" = "application/json"
  }
  Invoke-RestMethod -Uri "http://localhost:5000/cart/add" -Method Post -Headers $headers -Body '{"menu_item_id":1,"quantity":2}'
  ```
  ✅ Should add item to cart

### Test 6: Place Order (Protected)
- [ ] Place an order:
  ```powershell
  $orderData = @{
      items = @(
          @{menu_item_id = 1; quantity = 2}
      )
      delivery_address = "123 Test St"
      phone = "1234567890"
  } | ConvertTo-Json
  
  Invoke-RestMethod -Uri "http://localhost:5000/orders" -Method Post -Headers $headers -Body $orderData
  ```
  ✅ Should create order and return order details

---

## 📱 Step 7: Test with Postman (Optional)

- [ ] Install Postman (if not already installed)
- [ ] Create new collection "Food Ordering API"
- [ ] Add requests:
  - [ ] POST /auth/register
  - [ ] POST /auth/login
  - [ ] GET /restaurants
  - [ ] GET /restaurants/1/menu
  - [ ] POST /cart/add (with Bearer token)
  - [ ] GET /cart (with Bearer token)
  - [ ] POST /orders (with Bearer token)
  - [ ] GET /orders/history (with Bearer token)

---

## 🐛 Troubleshooting

### Issue: Cannot connect to database
- [ ] Check PostgreSQL is running: `pg_isready`
- [ ] Verify credentials in `.env` file
- [ ] Verify database exists: `psql -l`
- [ ] Check DATABASE_URL format in `.env`

### Issue: Module not found errors
- [ ] Ensure virtual environment is activated (see `(venv)` in terminal)
- [ ] Reinstall dependencies: `pip install -r requirements.txt`
- [ ] Check Python version: `python --version` (should be 3.8+)

### Issue: Migration errors
- [ ] Delete `migrations/` folder
- [ ] Re-run: `flask db init`, `flask db migrate`, `flask db upgrade`
- [ ] Ensure FLASK_APP is set: `$env:FLASK_APP="run.py"`

### Issue: Port 5000 already in use
- [ ] Change port in `run.py`: `app.run(port=5001)`
- [ ] Or kill process using port 5000

### Issue: JWT token errors
- [ ] Ensure JWT_SECRET_KEY is set in `.env`
- [ ] Check token format: `Bearer <token>`
- [ ] Token may be expired (default: 1 hour)

---

## 📚 Next Steps After Setup

- [ ] Read [README.md](README.md) for complete documentation
- [ ] Check [API_EXAMPLES.md](API_EXAMPLES.md) for API usage examples
- [ ] Review [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) to understand data structure
- [ ] Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for project overview

---

## 🎯 Ready for Frontend Integration

Once all tests pass:
- [ ] Share API endpoint (`http://localhost:5000`) with frontend team
- [ ] Update CORS_ORIGINS in `.env` with frontend URL
- [ ] Provide API documentation (API_EXAMPLES.md)
- [ ] Share test credentials:
  - Email: test@example.com
  - Password: password123

---

## 🔒 Security Checklist (Before Production)

- [ ] Change SECRET_KEY in `.env` to a strong random string
- [ ] Change JWT_SECRET_KEY in `.env` to a strong random string
- [ ] Set FLASK_ENV=production in `.env`
- [ ] Update CORS_ORIGINS to actual frontend domain
- [ ] Use HTTPS in production
- [ ] Set up proper database backups
- [ ] Add rate limiting
- [ ] Enable logging
- [ ] Add monitoring/error tracking

---

## ✨ Success Criteria

You've successfully set up the backend when:
- ✅ Flask server runs without errors
- ✅ Database tables are created
- ✅ Sample data is loaded (3 users, 5 restaurants, 25 menu items)
- ✅ You can register and login
- ✅ You can get restaurants list
- ✅ You can add items to cart with JWT token
- ✅ You can place orders with JWT token

---

## 📞 Quick Reference Commands

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run server
python run.py

# Run seed script
python seed.py

# Database migrations
flask db migrate -m "message"
flask db upgrade

# Deactivate virtual environment
deactivate
```

---

**Good luck with your Food Ordering App! 🍕🍔🍜**

Need help? Check the documentation files or test with the provided examples!
