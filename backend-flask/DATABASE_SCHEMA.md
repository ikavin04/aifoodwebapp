# Database Schema Documentation

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ name            │
│ email (unique)  │
│ password_hash   │
│ phone           │
│ address         │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │ 1
         │
         │ has many
         │
         ├──────────────────────┐
         │ *                    │ *
         │                      │
┌────────▼────────┐    ┌────────▼────────┐
│    ORDERS       │    │      CART       │
├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │
│ user_id (FK)    │    │ user_id (FK)    │
│ restaurant_id   │    │ menu_item_id(FK)│
│ total_amount    │    │ quantity        │
│ status          │    │ created_at      │
│ payment_method  │    │ updated_at      │
│ delivery_address│    └─────────────────┘
│ phone           │
│ notes           │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │ 1
         │
         │ has many
         │
         │ *
┌────────▼────────┐
│  ORDER_ITEMS    │
├─────────────────┤
│ id (PK)         │
│ order_id (FK)   │
│ menu_item_id(FK)│
│ quantity        │
│ price           │
│ created_at      │
└────────┬────────┘
         │
         │ belongs to
         │
         │ 1
┌────────▼────────┐
│   MENU_ITEMS    │
├─────────────────┤
│ id (PK)         │
│ restaurant_id(FK│
│ name            │
│ description     │
│ price           │
│ category        │
│ image_url       │
│ is_vegetarian   │
│ is_available    │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ belongs to
         │
         │ 1
┌────────▼────────┐
│  RESTAURANTS    │
├─────────────────┤
│ id (PK)         │
│ name            │
│ description     │
│ address         │
│ phone           │
│ image_url       │
│ cuisine_type    │
│ rating          │
│ delivery_time   │
│ is_active       │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

---

## 📋 Table Descriptions

### 1. USERS
**Purpose:** Store user account information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique user identifier |
| name | String(100) | Not Null | User's full name |
| email | String(120) | Unique, Not Null, Indexed | User's email (login) |
| password_hash | String(255) | Not Null | Hashed password |
| phone | String(20) | Nullable | Contact number |
| address | Text | Nullable | Default delivery address |
| created_at | DateTime | Default: now() | Account creation timestamp |
| updated_at | DateTime | Default: now(), Auto-update | Last modification timestamp |

**Relationships:**
- One-to-Many with Orders (one user can have many orders)
- One-to-Many with Cart (one user can have many cart items)

**Indexes:**
- email (unique index for fast login lookups)

---

### 2. RESTAURANTS
**Purpose:** Store restaurant information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique restaurant identifier |
| name | String(100) | Not Null | Restaurant name |
| description | Text | Nullable | Restaurant description |
| address | String(255) | Not Null | Physical address |
| phone | String(20) | Nullable | Contact number |
| image_url | String(500) | Nullable | Restaurant image URL |
| cuisine_type | String(50) | Nullable | Type of cuisine (Italian, Mexican, etc.) |
| rating | Float | Default: 0.0 | Average rating (0-5) |
| delivery_time | String(50) | Nullable | Estimated delivery time (e.g., "30-40 mins") |
| is_active | Boolean | Default: True | Whether restaurant is accepting orders |
| created_at | DateTime | Default: now() | Restaurant added timestamp |
| updated_at | DateTime | Default: now(), Auto-update | Last modification timestamp |

**Relationships:**
- One-to-Many with MenuItems (one restaurant has many menu items)
- One-to-Many with Orders (one restaurant can have many orders)

---

### 3. MENU_ITEMS
**Purpose:** Store food items available at restaurants

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique menu item identifier |
| restaurant_id | Integer | Foreign Key → restaurants.id, Not Null | Restaurant this item belongs to |
| name | String(100) | Not Null | Item name |
| description | Text | Nullable | Item description |
| price | Float | Not Null | Item price |
| category | String(50) | Nullable | Category (Pizza, Burger, Dessert, etc.) |
| image_url | String(500) | Nullable | Item image URL |
| is_vegetarian | Boolean | Default: False | Vegetarian flag |
| is_available | Boolean | Default: True | Currently available for order |
| created_at | DateTime | Default: now() | Item added timestamp |
| updated_at | DateTime | Default: now(), Auto-update | Last modification timestamp |

**Relationships:**
- Many-to-One with Restaurant (many items belong to one restaurant)
- One-to-Many with OrderItems
- One-to-Many with Cart

---

### 4. ORDERS
**Purpose:** Store customer orders

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique order identifier |
| user_id | Integer | Foreign Key → users.id, Not Null | User who placed the order |
| restaurant_id | Integer | Foreign Key → restaurants.id, Not Null | Restaurant order is from |
| total_amount | Float | Not Null | Total order amount |
| status | String(50) | Default: 'pending' | Order status |
| payment_method | String(50) | Default: 'cash_on_delivery' | Payment method |
| delivery_address | Text | Not Null | Delivery address for this order |
| phone | String(20) | Not Null | Contact number for delivery |
| notes | Text | Nullable | Special instructions |
| created_at | DateTime | Default: now() | Order placed timestamp |
| updated_at | DateTime | Default: now(), Auto-update | Last status update timestamp |

**Status Values:**
- `pending` - Order placed, awaiting confirmation
- `confirmed` - Restaurant confirmed the order
- `preparing` - Food is being prepared
- `out_for_delivery` - Order is on the way
- `delivered` - Order successfully delivered
- `cancelled` - Order was cancelled

**Relationships:**
- Many-to-One with User (many orders belong to one user)
- Many-to-One with Restaurant (many orders can be from one restaurant)
- One-to-Many with OrderItems (one order contains many items)

---

### 5. ORDER_ITEMS
**Purpose:** Junction table linking orders to menu items (with quantity and price snapshot)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique order item identifier |
| order_id | Integer | Foreign Key → orders.id, Not Null | Order this item belongs to |
| menu_item_id | Integer | Foreign Key → menu_items.id, Not Null | Menu item ordered |
| quantity | Integer | Not Null, Default: 1 | Quantity ordered |
| price | Float | Not Null | Price at time of order (snapshot) |
| created_at | DateTime | Default: now() | Item added timestamp |

**Why price is stored:**
Menu item prices may change over time. We store the price at the time of order to maintain accurate historical records.

**Relationships:**
- Many-to-One with Order (many items in one order)
- Many-to-One with MenuItem (reference to the menu item)

---

### 6. CART
**Purpose:** Store items in user's shopping cart

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique cart item identifier |
| user_id | Integer | Foreign Key → users.id, Not Null | User who owns this cart item |
| menu_item_id | Integer | Foreign Key → menu_items.id, Not Null | Menu item in cart |
| quantity | Integer | Not Null, Default: 1 | Quantity in cart |
| created_at | DateTime | Default: now() | Item added to cart timestamp |
| updated_at | DateTime | Default: now(), Auto-update | Last quantity update timestamp |

**Relationships:**
- Many-to-One with User (many cart items belong to one user)
- Many-to-One with MenuItem (reference to the menu item)

**Note:** Cart is cleared when order is successfully placed

---

## 🔑 Foreign Key Relationships

```sql
-- Order relationships
orders.user_id → users.id (ON DELETE CASCADE)
orders.restaurant_id → restaurants.id

-- Order items relationships
order_items.order_id → orders.id (ON DELETE CASCADE)
order_items.menu_item_id → menu_items.id

-- Menu items relationships
menu_items.restaurant_id → restaurants.id (ON DELETE CASCADE)

-- Cart relationships
cart.user_id → users.id (ON DELETE CASCADE)
cart.menu_item_id → menu_items.id
```

---

## 🔍 Indexes (for query optimization)

1. **users.email** - Unique index for fast login lookups
2. **orders.user_id** - Index for user's order history
3. **order_items.order_id** - Index for order details
4. **menu_items.restaurant_id** - Index for restaurant menus
5. **cart.user_id** - Index for user's cart

---

## 📊 Sample Data Counts (After Seeding)

| Table | Count | Description |
|-------|-------|-------------|
| users | 3 | Sample users with test credentials |
| restaurants | 5 | Various cuisine types |
| menu_items | 25 | 5 items per restaurant |
| orders | 0 | No pre-seeded orders |
| order_items | 0 | Created when orders are placed |
| cart | 0 | Empty initially |

---

## 🔐 Data Integrity Rules

1. **User cannot be deleted if they have orders**
   - Solution: Use soft delete or archive orders first

2. **Restaurant deletion cascades to menu items**
   - All menu items are deleted when restaurant is deleted

3. **Order deletion cascades to order items**
   - All order items are deleted when order is deleted

4. **Menu item price changes don't affect past orders**
   - Order items store price snapshot

5. **All items in an order must be from the same restaurant**
   - Validated in application logic

6. **Cart is cleared after successful order**
   - Handled in OrderService

---

## 📈 Common Queries

### Get user's order history
```sql
SELECT * FROM orders 
WHERE user_id = ? 
ORDER BY created_at DESC;
```

### Get restaurant menu
```sql
SELECT * FROM menu_items 
WHERE restaurant_id = ? AND is_available = true;
```

### Get order details with items
```sql
SELECT o.*, oi.*, mi.name 
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN menu_items mi ON oi.menu_item_id = mi.id
WHERE o.id = ?;
```

### Get user's cart with total
```sql
SELECT c.*, mi.name, mi.price, (c.quantity * mi.price) as subtotal
FROM cart c
JOIN menu_items mi ON c.menu_item_id = mi.id
WHERE c.user_id = ?;
```

---

## 🛠️ Migration Commands

```bash
# Initialize migrations
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# Show current migration version
flask db current

# Show migration history
flask db history
```

---

## 💾 Database Backup Strategy

### Development:
```bash
# Backup
pg_dump foodorder_db > backup_$(date +%Y%m%d).sql

# Restore
psql foodorder_db < backup_20260122.sql
```

### Production:
- Automated daily backups
- Point-in-time recovery enabled
- Backup retention: 30 days
- Test restore procedures monthly

---

## 📊 Performance Considerations

1. **Indexes** - Created on frequently queried columns (email, foreign keys)
2. **Cascade deletes** - Properly configured to maintain referential integrity
3. **Price snapshots** - Order items store price to avoid joins with menu_items
4. **Query optimization** - SQLAlchemy lazy loading configured appropriately
5. **Connection pooling** - SQLAlchemy handles connection pooling

---

**Database schema designed for scalability, performance, and data integrity!**
