# Address Management Feature - Setup Guide

## Overview
This feature implements a comprehensive address management system similar to Swiggy and Zomato, allowing users to:
- Add multiple delivery addresses
- Select address from saved addresses
- View address at the top of the navbar
- Filter restaurants by city based on selected address
- Change address while ordering
- Set default addresses

## Backend Changes

### 1. Database Models

#### New Model: `UserAddress`
Located in: `backend-flask/app/models/__init__.py`

Fields:
- `id`: Primary key
- `user_id`: Foreign key to users
- `label`: Address type (Home, Work, Other)
- `address_line1`: Main address line
- `address_line2`: Additional address info (optional)
- `city`: City name (used for filtering restaurants)
- `state`: State name
- `pincode`: Postal code
- `landmark`: Nearby landmark (optional)
- `phone`: Contact phone (optional)
- `is_default`: Default address flag
- `created_at`, `updated_at`: Timestamps

#### Updated Models:
- **User**: Added `current_address_id` field and `addresses` relationship
- **Restaurant**: Added `city`, `state`, `pincode` fields for location-based filtering

### 2. New Routes & Services

#### Address Routes (`backend-flask/app/routes/address.py`)
- `GET /addresses` - Get all user addresses
- `POST /addresses` - Create new address
- `PUT /addresses/<id>` - Update address
- `DELETE /addresses/<id>` - Delete address
- `PUT /addresses/<id>/set-default` - Set as default
- `PUT /addresses/current` - Set current browsing address

#### Address Service (`backend-flask/app/services/address_service.py`)
Handles all address-related business logic

#### Updated Restaurant Service
- Added city filtering to `search_restaurants()` method

### 3. Database Migration
File: `backend-flask/migrations/versions/add_user_addresses.py`

To apply migration:
```bash
cd backend-flask
flask db upgrade
```

## Frontend Changes

### 1. New Components

#### AddressModal (`src/components/AddressModal.jsx`)
- Beautiful modal for adding/editing addresses
- Form validation
- Address type selection (Home, Work, Other)
- All address fields with proper validation

#### AddressPicker (`src/components/AddressPicker.jsx`)
- Dropdown component for address selection
- Shows current address with city and state
- List of all saved addresses
- Quick add new address button
- Delete address functionality

### 2. Updated Components

#### Navbar (`src/components/Navbar.jsx`)
- Integrated AddressPicker at the top
- Shows address prominently (desktop: center, mobile: below navbar)
- Address change triggers restaurant refresh

#### Home Page (`src/pages/Home.jsx`)
- Listens for address changes
- Filters restaurants by selected city
- Shows current city in header
- Auto-loads restaurants for default address

#### Checkout Page (`src/pages/Checkout.jsx`)
- Completely redesigned to use saved addresses
- Address selection interface
- Auto-selects default address
- "Add New Address" option during checkout
- Delivery instructions field

### 3. API Service Updates (`src/services/api.js`)
Added new `addressAPI` with methods:
- `getAll()` - Fetch all addresses
- `create(data)` - Create address
- `update(id, data)` - Update address
- `delete(id)` - Delete address
- `setDefault(id)` - Set default
- `setCurrent(id)` - Set current for browsing

## Usage Flow

### First Time User:
1. User logs in
2. Navbar shows "Add Address" button
3. User clicks and fills address modal
4. Address is saved and set as current
5. Restaurants filtered by address city
6. Address appears in navbar

### Returning User:
1. User logs in
2. Default address automatically loads in navbar
3. Restaurants filtered by default address city
4. User can change address anytime via navbar dropdown
5. Restaurant list updates automatically

### During Checkout:
1. Default address auto-selected
2. User can change to another saved address
3. User can add new address if needed
4. Address used for order delivery

### Changing Address:
1. Click address in navbar
2. Dropdown shows all saved addresses
3. Select different address
4. Restaurant list refreshes for new city
5. Selected address becomes current

## Key Features

### 1. Address Persistence
- Addresses saved to database
- Linked to user account
- Available across sessions

### 2. City-Based Filtering
- Restaurants filtered by address city
- Backend supports city parameter
- Mock data includes city field

### 3. Default Address
- First address automatically default
- User can change default anytime
- Default used for checkout

### 4. Current Address
- Separate from default
- Used for browsing restaurants
- Persists until changed

### 5. Smart UI/UX
- Address visible at top (like Swiggy/Zomato)
- Easy address switching
- Visual feedback for selected address
- Mobile responsive design

## Testing the Feature

### Backend Testing:
```bash
cd backend-flask
# Run migrations
flask db upgrade

# Start backend
python run.py
```

### Frontend Testing:
```bash
# Start frontend
npm run dev
```

### Test Scenarios:
1. **Add First Address**: Login → Click "Add Address" → Fill form → Save
2. **Add Multiple Addresses**: Navbar → Add multiple Home/Work/Other addresses
3. **Change Address**: Navbar dropdown → Select different address → See restaurants update
4. **Checkout Flow**: Add items → Checkout → See saved addresses → Select address → Place order
5. **Delete Address**: Navbar dropdown → Hover address → Click delete
6. **Edit Address**: Can be added by extending the AddressPicker component

## API Endpoints Reference

### Address Endpoints:
```
GET    /addresses              - Get all user addresses
POST   /addresses              - Create new address
PUT    /addresses/:id          - Update address
DELETE /addresses/:id          - Delete address
PUT    /addresses/:id/set-default - Set default address
PUT    /addresses/current      - Set current address
```

### Restaurant Endpoints:
```
GET /restaurants?city=Mumbai   - Get restaurants by city
```

## Database Schema

### user_addresses Table:
```sql
CREATE TABLE user_addresses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    label VARCHAR(50) NOT NULL,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(20) NOT NULL,
    landmark VARCHAR(255),
    phone VARCHAR(20),
    is_default BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Configuration Notes

1. **Mock Data**: Frontend works with mock data if backend unavailable
2. **Token Storage**: Uses localStorage for JWT tokens
3. **Auto-refresh**: Address changes trigger event-based refresh
4. **Validation**: Both frontend and backend validation

## Future Enhancements

1. Edit address functionality in AddressPicker
2. GPS/Map integration for address selection
3. Address auto-complete
4. Distance-based restaurant sorting
5. Delivery area validation
6. Multiple delivery slots

## Troubleshooting

### Restaurants not filtering by city:
- Check if address has city field
- Verify addressChanged event is triggered
- Check backend city parameter

### Address not showing in navbar:
- Verify user has saved addresses
- Check token in localStorage
- Verify API endpoint returns addresses

### Cannot add address:
- Check form validation
- Verify backend route is registered
- Check JWT token is valid

## Files Modified/Created

### Backend:
- ✅ `app/models/__init__.py` - Added UserAddress model
- ✅ `app/routes/address.py` - New address routes
- ✅ `app/services/address_service.py` - New address service
- ✅ `app/services/restaurant_service.py` - Updated with city filter
- ✅ `app/__init__.py` - Registered address blueprint
- ✅ `migrations/versions/add_user_addresses.py` - New migration

### Frontend:
- ✅ `src/components/AddressModal.jsx` - New component
- ✅ `src/components/AddressPicker.jsx` - New component
- ✅ `src/components/Navbar.jsx` - Updated with address picker
- ✅ `src/pages/Home.jsx` - Updated with city filtering
- ✅ `src/pages/Checkout.jsx` - Redesigned with address selection
- ✅ `src/services/api.js` - Added addressAPI

## Summary

This implementation provides a complete address management system that:
✅ Shows address at the top like Swiggy/Zomato
✅ Supports multiple addresses per user
✅ Filters restaurants by selected address city
✅ Remembers user's address preference
✅ Allows address change during ordering
✅ Beautiful, intuitive UI/UX
✅ Mobile responsive
✅ Production-ready code
