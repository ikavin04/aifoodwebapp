# Testing the AI Order Feature

## Setup
1. ✅ Backend Flask server running on http://localhost:5000
2. ✅ Frontend Vite dev server running on http://localhost:3000
3. ✅ Database seeded with restaurants and menu items

## Test Steps

### 1. Login/Register
- Open http://localhost:3000
- Login with your account or register a new one
- **Important:** Make sure your profile has:
  - Delivery address set
  - Phone number set

### 2. Navigate to AI Assistant
- Click "AI Assistant" in the navigation bar
- You should see the AI welcome message

### 3. Test Order Commands

Try these example commands:

#### Example 1: Pizza Palace Order
```
Place order for Margherita Pizza from Pizza Palace with cash on delivery
```

#### Example 2: Short Form
```
Order Garlic Bread from Pizza Palace with COD
```

#### Example 3: Different Restaurant
```
Get me Chicken Biryani from Anjappar with cash
```

#### Example 4: Alternative Phrasing
```
I want to order Mutton Biryani from Hotel Junior Kuppanna using cash on delivery
```

### 4. Verify Order Placement

After sending a command, you should see:
1. ✅ AI confirmation message
2. ✅ Order card showing:
   - Order ID
   - Dish name
   - Restaurant name
   - Price
   - Payment method
   - Status (pending)
3. ✅ "View Order Details" button

### 5. Check Orders Page
- Click "View Order Details" button OR
- Navigate to "Orders" in the navigation
- Verify your order appears in the order history

## Expected Behavior

### Success Case
```
User: Place order for Margherita Pizza from Pizza Palace with cash on delivery

AI: Great! I've placed your order for Margherita Pizza from Pizza Palace 
    with cash on delivery. Your order will arrive soon!
    
[Order Confirmation Card showing all details]
```

### Error Cases

#### Dish Not Found
```
User: Place order for XYZ Dish from Pizza Palace with COD

AI: Sorry, I couldn't find 'XYZ Dish' at Pizza Palace. 
    Please check the menu and try again.
```

#### Profile Incomplete
```
User: Place order for Pizza from Pizza Palace with COD

AI: Please update your profile with delivery address and phone number 
    before placing an order.
```

## Debugging

### If orders aren't placing:
1. Check browser console for errors (F12)
2. Check Flask terminal for backend errors
3. Verify you're logged in (check token in localStorage)
4. Verify database has restaurants and menu items

### If AI doesn't understand:
- Make sure to include dish name, restaurant name
- Use clear food keywords (pizza, biryani, bread, etc.)
- Include "order" or "place order" in the command

## API Endpoint
The AI order feature uses:
- **Endpoint:** POST /ai/order-assistant
- **Auth:** Requires JWT token
- **Body:** `{ "message": "your order command" }`

## Sample Restaurants in Database
Based on the seed data, available restaurants include:
- Pizza Palace
- Anjappar Chettinad
- Hotel Junior Kuppanna
- Shree Annapoorna
- Haribhavanam
- And more...

Check the home page to see all available restaurants and their menus before testing!
