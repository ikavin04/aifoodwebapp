# Quick Start Guide - Address Management Feature

## 🚀 Getting Started in 3 Steps

### Step 1: Run Database Migration
```bash
cd backend-flask
flask db upgrade
```

### Step 2: Start Backend Server
```bash
cd backend-flask
python run.py
```

### Step 3: Start Frontend
```bash
npm run dev
```

## 🎯 Test the Feature

### 1. Add Your First Address
- Login to the app
- Look at the top navbar
- Click "Add Address" button
- Fill in the form:
  - Select type: Home/Work/Other
  - Enter house/flat number
  - Enter area/apartment name
  - Add landmark (optional)
  - Enter City (e.g., Mumbai)
  - Enter State (e.g., Maharashtra)
  - Enter Pincode (6 digits)
  - Add phone (optional)
- Click "Save Address"

### 2. See Restaurants Filtered by City
- After adding address, you'll see restaurants for that city
- The header shows: "Showing restaurants in [Your City]"
- All restaurants match your address city

### 3. Add More Addresses
- Click the address dropdown in navbar
- Click "Add New Address"
- Add Work address, Other addresses, etc.

### 4. Switch Between Addresses
- Click address dropdown in navbar
- Select any saved address
- Watch restaurants update to match new city

### 5. Place an Order
- Add items to cart
- Go to Checkout
- Your default address is auto-selected
- Can change to another saved address
- Or add new address if needed
- Add delivery instructions
- Place order

## 🎨 UI Overview

```
┌─────────────────────────────────────────────────┐
│  🏠 AI FoodApp    [📍 Home, Mumbai, MH ▼]   🛒 │  ← Navbar with Address
└─────────────────────────────────────────────────┘
│ Order Food Online                               │
│ 📍 Showing restaurants in Mumbai               │  ← City indicator
│                                                 │
│ [Search...]                                     │
│                                                 │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│ │ Pizza   │ │ Burger  │ │ Biryani │          │  ← Filtered by city
│ │ Palace  │ │ King    │ │ House   │          │
│ └─────────┘ └─────────┘ └─────────┘          │
```

## 📋 Address Dropdown Preview

```
┌──────────────────────────────────────┐
│ Select Delivery Address              │
├──────────────────────────────────────┤
│ ✓ 🏠 Home                    [Default]│
│   123, Green Valley Apartments      │
│   Mumbai, Maharashtra - 400001      │
│   Near: City Hospital               │
├──────────────────────────────────────┤
│   💼 Work                            │
│   456, Tech Park, Andheri          │
│   Mumbai, Maharashtra - 400053      │
├──────────────────────────────────────┤
│ [+ Add New Address]                 │
└──────────────────────────────────────┘
```

## ✅ Feature Checklist

After setup, verify these work:

- [ ] Can add first address
- [ ] Address appears in navbar at top
- [ ] Restaurants filtered by address city
- [ ] Can add multiple addresses
- [ ] Can switch between addresses
- [ ] Restaurants update when address changes
- [ ] Checkout shows saved addresses
- [ ] Can select address at checkout
- [ ] Can add new address during checkout
- [ ] Address persists after logout/login

## 🐛 Common Issues & Solutions

### Issue: "Add Address" not showing
**Solution**: Make sure you're logged in. Address feature requires authentication.

### Issue: Restaurants not filtering by city
**Solution**: 
1. Check if address has city field filled
2. Wait a moment for restaurants to refresh
3. Check browser console for errors

### Issue: Can't add address
**Solution**:
1. Fill all required fields (marked with *)
2. Pincode must be 6 digits
3. Check backend is running

### Issue: Address not appearing in navbar
**Solution**:
1. Refresh the page
2. Check if address was saved (open dropdown)
3. Verify JWT token in localStorage

## 📱 Mobile Experience

The feature is fully responsive:
- Address picker appears below navbar on mobile
- Dropdown is touch-friendly
- Modal scrolls smoothly
- All features work on small screens

## 🎓 Tips for Best Experience

1. **Add addresses with different cities** to see filtering in action
2. **Set one as default** for quick checkout
3. **Add landmarks** for easier delivery
4. **Use descriptive labels** (Home, Office, Parent's House, etc.)
5. **Keep phone numbers** updated for delivery contact

## 🔄 Update Your Existing Data

If you have existing restaurants in database, update them with cities:

```sql
UPDATE restaurants SET 
  city = 'Mumbai', 
  state = 'Maharashtra', 
  pincode = '400001' 
WHERE id = 1;

UPDATE restaurants SET 
  city = 'Delhi', 
  state = 'Delhi', 
  pincode = '110001' 
WHERE id = 2;
```

## 📞 Need Help?

1. Check `ADDRESS_FEATURE_GUIDE.md` for detailed documentation
2. Check `ADDRESS_IMPLEMENTATION_SUMMARY.md` for implementation details
3. Review browser console for errors
4. Check backend terminal for API errors

## 🎉 Enjoy Your New Feature!

Your food ordering app now has professional-grade address management just like Swiggy and Zomato! 🚀
