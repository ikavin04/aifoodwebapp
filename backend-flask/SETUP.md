# Quick Setup Guide for Flask Food Ordering Backend

## Follow these steps to get started:

### 1. Install Python Dependencies
```powershell
cd backend-flask
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup PostgreSQL Database
Make sure PostgreSQL is installed and running, then create the database:
```sql
CREATE DATABASE foodorder_db;
```

### 3. Configure Environment Variables
Update the `.env` file with your database credentials:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/foodorder_db
```

### 4. Initialize Database
```powershell
# Set Flask app
$env:FLASK_APP="run.py"

# Initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Seed Sample Data
```powershell
python seed.py
```

### 6. Run the Application
```powershell
python run.py
```

The API will be running at: http://localhost:5000

### 7. Test the API
Visit: http://localhost:5000/health

Or test with login:
```powershell
# Register a new user
curl -X POST http://localhost:5000/auth/register -H "Content-Type: application/json" -d '{\"name\":\"Test User\",\"email\":\"test@test.com\",\"password\":\"test123\"}'

# Login
curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{\"email\":\"test@test.com\",\"password\":\"test123\"}'
```

### Default Test Credentials
- Email: test@example.com
- Password: password123

## API Endpoints Overview

### Public Endpoints:
- POST /auth/register - Register new user
- POST /auth/login - User login
- GET /restaurants - List all restaurants
- GET /restaurants/{id}/menu - Get restaurant menu

### Protected Endpoints (requires JWT token):
- GET /auth/me - Get current user
- POST /cart/add - Add item to cart
- GET /cart - View cart
- POST /orders - Place order
- GET /orders/history - Order history

## Troubleshooting

### Database Connection Issues:
- Ensure PostgreSQL is running
- Check database credentials in .env file
- Verify database exists: `psql -l`

### Import Errors:
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Migration Issues:
- Delete migrations folder and reinitialize
- Make sure FLASK_APP environment variable is set

## Next Steps

1. Test all API endpoints using Postman or cURL
2. Integrate with your frontend application
3. Add additional features as needed
4. Deploy to production server

Happy Coding! 🚀
