# AI Order Assistant - Natural Language Ordering

## Overview
The AI Assistant can now automatically place orders based on natural language commands! Just tell the AI what you want, and it will handle the entire order process for you.

## How to Use

### Basic Command Structure
```
Place order for [DISH NAME] from [RESTAURANT NAME] with [PAYMENT METHOD]
```

### Example Commands

1. **Full Order Command:**
   ```
   Place order for Margherita Pizza from Pizza Palace with cash on delivery
   ```

2. **Short Form:**
   ```
   Order Chicken Biryani from Biryani House with COD
   ```

3. **Alternative Phrasings:**
   ```
   Get me Garlic Bread from Pizza Palace using cash on delivery
   Buy Mutton Biryani from Anjappar with cash
   I want to order Pepperoni Pizza from Dominos with COD
   ```

### Supported Payment Methods
- `cash on delivery` / `COD` / `cash` → Cash on Delivery
- `card` / `credit card` / `debit card` → Card Payment
- `upi` / `online` → Online Payment

## Features

✅ **Natural Language Understanding** - AI parses your command intelligently
✅ **Restaurant Matching** - Finds the restaurant by name (fuzzy matching)
✅ **Dish Recognition** - Identifies menu items from your description
✅ **Payment Method Selection** - Supports multiple payment options
✅ **Order Confirmation** - Shows detailed order confirmation with order ID
✅ **Order Tracking** - Direct link to view order details

## What You'll See

When you place an order through AI, you'll receive:

1. **Confirmation Message** from the AI
2. **Order Card** showing:
   - Order ID
   - Dish Name
   - Restaurant Name
   - Price
   - Payment Method
   - Order Status
3. **View Order Button** to check order details

## Prerequisites

Before using AI ordering, make sure:
- You're logged in
- Your profile has a delivery address set
- Your profile has a phone number set

If these are missing, the AI will prompt you to update your profile first.

## Tips

- Be specific with dish names (e.g., "Margherita Pizza" instead of just "pizza")
- Include restaurant name for accurate ordering
- Specify payment method explicitly for your preferred option
- Default payment method is Cash on Delivery if not specified

## Error Handling

The AI will help you if:
- The dish is not found → Suggests checking the menu
- Restaurant doesn't have the dish → Offers alternatives
- Profile incomplete → Prompts to update profile
- Payment method unclear → Uses Cash on Delivery as default

## Example Conversation

```
You: Place order for Margherita Pizza from Pizza Palace with cash on delivery

AI: Great! I've placed your order for Margherita Pizza from Pizza Palace 
    with cash on delivery. Your order will arrive soon!
    
    [Order Card with details]
```

## Note

This feature requires:
- Backend Flask server running
- Database with restaurants and menu items seeded
- Valid user session (logged in)
