# Address Management System - Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Navbar     │  │  Home Page   │  │   Checkout   │     │
│  │              │  │              │  │              │     │
│  │ - Address    │  │ - Restaurant │  │ - Address    │     │
│  │   Picker     │  │   List       │  │   Selection  │     │
│  │ - Dropdown   │  │ - City       │  │ - Delivery   │     │
│  └──────┬───────┘  │   Filter     │  │   Details    │     │
│         │          └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │             │
│  ┌──────▼─────────────────▼──────────────────▼───────┐    │
│  │          AddressPicker Component                   │    │
│  │  - Displays current address                        │    │
│  │  - Lists all saved addresses                       │    │
│  │  - Triggers address change events                  │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│  ┌────────────────────▼───────────────────────────────┐    │
│  │          AddressModal Component                     │    │
│  │  - Form for adding/editing addresses               │    │
│  │  - Validation                                       │    │
│  │  - Submit to API                                    │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        │ API Calls (axios)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    BACKEND (Flask)                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Address Routes (/addresses)            │    │
│  │                                                      │    │
│  │  GET    /addresses           → Get all addresses   │    │
│  │  POST   /addresses           → Create address      │    │
│  │  PUT    /addresses/:id       → Update address      │    │
│  │  DELETE /addresses/:id       → Delete address      │    │
│  │  PUT    /addresses/:id/set-default → Set default   │    │
│  │  PUT    /addresses/current   → Set current         │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│  ┌────────────────────▼───────────────────────────────┐    │
│  │            Address Service                          │    │
│  │  - Business logic for address management           │    │
│  │  - Validation                                       │    │
│  │  - Database operations                              │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│  ┌────────────────────▼───────────────────────────────┐    │
│  │         Restaurant Service (Updated)                │    │
│  │  - Filter restaurants by city                      │    │
│  │  - Search with location awareness                  │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        │ SQLAlchemy ORM
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                     DATABASE (SQLite/PostgreSQL)             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    users     │  │user_addresses│  │ restaurants  │     │
│  │              │  │              │  │              │     │
│  │ - id         │  │ - id         │  │ - id         │     │
│  │ - name       │◄─┤ - user_id    │  │ - name       │     │
│  │ - email      │  │ - label      │  │ - city       │     │
│  │ - current_   │  │ - address_   │  │ - state      │     │
│  │   address_id ├─►│   line1      │  │ - pincode    │     │
│  └──────────────┘  │ - address_   │  └──────────────┘     │
│                    │   line2      │                        │
│                    │ - city       │                        │
│                    │ - state      │                        │
│                    │ - pincode    │                        │
│                    │ - landmark   │                        │
│                    │ - is_default │                        │
│                    └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## User Flow Diagram

```
                    ┌─────────────┐
                    │   LOGIN     │
                    └──────┬──────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Has Saved Address?   │
                └──────┬───────┬───────┘
                       │       │
                  YES  │       │  NO
                       │       │
                       ▼       ▼
        ┌──────────────┐   ┌──────────────┐
        │ Load Default │   │ Show "Add    │
        │ Address      │   │ Address" btn │
        └──────┬───────┘   └──────┬───────┘
               │                  │
               │                  ▼
               │           ┌──────────────┐
               │           │ User Fills   │
               │           │ Address Form │
               │           └──────┬───────┘
               │                  │
               ▼                  ▼
        ┌─────────────────────────────┐
        │ Address Shown in Navbar     │
        │ (City, State displayed)     │
        └──────────┬──────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │ Restaurants Filtered by     │
        │ Address City                │
        └──────────┬──────────────────┘
                   │
                   ├──────────┐
                   │          │
        ┌──────────▼──────┐   │
        │ Browse & Add to │   │
        │ Cart            │   │
        └──────────┬──────┘   │
                   │          │
                   ▼          │ Change Address?
        ┌─────────────────┐  │
        │ Go to Checkout  │  │
        └──────────┬──────┘  │
                   │          │
                   ▼          │
        ┌─────────────────────────┐
        │ Select Delivery Address │
        │ (Default pre-selected)  │
        └──────────┬──────────────┘
                   │
                   ├──────────┐
                   │          │
        ┌──────────▼──────┐   │ Change?
        │ Place Order     │   │
        └─────────────────┘   │
                              │
              ┌───────────────┘
              │
              ▼
   ┌────────────────────────┐
   │ Click Address Dropdown │
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │ Select Different       │
   │ Address                │
   └──────────┬─────────────┘
              │
              ▼
   ┌────────────────────────┐
   │ Restaurants Refresh    │
   │ for New City           │
   └────────────────────────┘
```

## Address Change Event Flow

```
User clicks address in navbar
         │
         ▼
┌─────────────────────┐
│ AddressPicker opens │
│ dropdown            │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ User selects        │
│ different address   │
└─────────┬───────────┘
          │
          ▼
┌──────────────────────┐
│ API Call:            │
│ PUT /addresses/      │
│     current          │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Backend updates      │
│ user.current_        │
│ address_id           │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Frontend dispatches  │
│ 'addressChanged'     │
│ event                │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Home component       │
│ listens to event     │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Fetch restaurants    │
│ with new city filter │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Restaurant list      │
│ updates on page      │
└──────────────────────┘
```

## Checkout Flow

```
User clicks Checkout
         │
         ▼
┌─────────────────────┐
│ Checkout page loads │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Fetch all saved     │
│ addresses           │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Auto-select default │
│ address             │
└─────────┬───────────┘
          │
          ├───────────────────┐
          │                   │
          ▼                   │ Need new address?
┌─────────────────────┐       │
│ User reviews order  │       │
│ and address         │       │
└─────────┬───────────┘       │
          │                   │
          ▼                   ▼
┌─────────────────────┐  ┌──────────────┐
│ Places order with   │  │ Click "Add   │
│ selected address    │  │ New Address" │
└─────────────────────┘  └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ AddressModal │
                         │ opens        │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ Fill & Save  │
                         │ address      │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ New address  │
                         │ appears in   │
                         │ list         │
                         └──────────────┘
```

## Data Flow

```
┌────────────────────────────────────────────────────────┐
│                    ADDRESS CREATION                     │
└────────────────────────────────────────────────────────┘

Frontend                      Backend                 Database
   │                             │                        │
   │  POST /addresses            │                        │
   ├────────────────────────────►│                        │
   │  {                          │                        │
   │    label: "Home",           │  Validate data         │
   │    address_line1: "...",    ├───────────┐            │
   │    city: "Mumbai",          │           │            │
   │    state: "Maharashtra",    │           │            │
   │    pincode: "400001",       │           │            │
   │    is_default: true         │           │            │
   │  }                          │           │            │
   │                             │           │            │
   │                             │◄──────────┘            │
   │                             │                        │
   │                             │  Create UserAddress    │
   │                             ├───────────────────────►│
   │                             │                        │
   │                             │  If first address      │
   │                             │  or is_default=true:   │
   │                             │  - Set as default      │
   │                             │  - Set as current      │
   │                             │  - Update user         │
   │                             ├───────────────────────►│
   │                             │                        │
   │                             │  Return saved address  │
   │                             │◄───────────────────────┤
   │                             │                        │
   │  { address: {...} }         │                        │
   │◄────────────────────────────┤                        │
   │                             │                        │
   │  Update UI                  │                        │
   ├────────────┐                │                        │
   │            │                │                        │
   │  - Show in │                │                        │
   │    navbar  │                │                        │
   │  - Trigger │                │                        │
   │    restaurant               │                        │
   │    refresh │                │                        │
   │◄───────────┘                │                        │


┌────────────────────────────────────────────────────────┐
│               RESTAURANT FILTERING BY CITY              │
└────────────────────────────────────────────────────────┘

Frontend                      Backend                 Database
   │                             │                        │
   │  GET /restaurants?          │                        │
   │      city=Mumbai            │                        │
   ├────────────────────────────►│                        │
   │                             │                        │
   │                             │  Query restaurants     │
   │                             │  WHERE city LIKE       │
   │                             │  '%Mumbai%'            │
   │                             ├───────────────────────►│
   │                             │                        │
   │                             │  Return matching       │
   │                             │  restaurants           │
   │                             │◄───────────────────────┤
   │                             │                        │
   │  { restaurants: [...] }     │                        │
   │◄────────────────────────────┤                        │
   │                             │                        │
   │  Render restaurant cards    │                        │
   ├────────────┐                │                        │
   │            │                │                        │
   │  Display   │                │                        │
   │  only      │                │                        │
   │  Mumbai    │                │                        │
   │  restaurants                │                        │
   │◄───────────┘                │                        │
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────┐
│                        Navbar                             │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │            AddressPicker                         │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │  📍 Home, Mumbai, MH ▼                    │   │    │
│  │  └──────────────┬───────────────────────────┘   │    │
│  │                 │ onClick                        │    │
│  │                 ▼                                │    │
│  │  ┌──────────────────────────────────────────┐   │    │
│  │  │  Dropdown with all addresses             │   │    │
│  │  │  - ✓ Home (selected)                     │   │    │
│  │  │  - Work                                   │   │    │
│  │  │  - Other                                  │   │    │
│  │  │  [+ Add New Address]                     │   │    │
│  │  └──────────────┬───────────────────────────┘   │    │
│  │                 │ onSelect                       │    │
│  │                 ▼                                │    │
│  │         Update current address                  │    │
│  │         Dispatch 'addressChanged' event         │    │
│  └─────────────────┬───────────────────────────────┘    │
└────────────────────┼──────────────────────────────────────┘
                     │
                     │ Custom Event
                     │
┌────────────────────▼──────────────────────────────────────┐
│                        Home Page                          │
│                                                           │
│  useEffect(() => {                                       │
│    window.addEventListener('addressChanged', handler);   │
│  }, []);                                                 │
│                                                           │
│  const handler = (event) => {                            │
│    const address = event.detail;                         │
│    fetchRestaurants(address.city);                       │
│  };                                                       │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Restaurant Grid (filtered by city)             │    │
│  │  [Pizza Palace] [Burger King] [Biryani House]   │    │
│  └─────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────┘
```

This architecture ensures:
- ✅ Clean separation of concerns
- ✅ Reusable components
- ✅ Event-driven updates
- ✅ Database normalization
- ✅ RESTful API design
- ✅ Scalable structure
