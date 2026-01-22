# AI Food Ordering Web App

A modern food ordering web application with AI-powered assistance, built with React and Tailwind CSS.

## Features

✨ **Core Features:**
- User Authentication (Login/Register with JWT)
- Restaurant Browsing with Search & Filters
- Menu Viewing with Categories
- Shopping Cart Management
- Checkout with COD Payment
- Order History Tracking
- **AI Assistant** - Text-based food ordering assistant with smart suggestions

🤖 **AI Assistant Features:**
- Natural language food ordering
- Smart recommendations:
  - **Cheapest** - Best price options
  - **Fastest** - Quick delivery
  - **Best Rated** - Top-rated restaurants
- Chat interface with conversation history
- Direct cart integration from AI suggestions

## Tech Stack

- **Frontend:** React 18 + Vite
- **Routing:** React Router v6
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **HTTP Client:** Axios
- **State Management:** Context API
- **Auth:** JWT stored in localStorage

## Project Structure

```
aifoodwebapp/
├── src/
│   ├── components/
│   │   └── Navbar.jsx
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── CartContext.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Home.jsx
│   │   ├── Restaurant.jsx
│   │   ├── Cart.jsx
│   │   ├── Checkout.jsx
│   │   ├── Orders.jsx
│   │   └── AIAssistant.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to:
```
http://localhost:3000
```

### Build for Production

```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## API Integration

The app expects a Flask backend running on `http://localhost:5000` with the following endpoints:

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Restaurants
- `GET /restaurants` - Get all restaurants (supports search/filter params)
- `GET /restaurants/:id` - Get restaurant details
- `GET /restaurants/:id/menu` - Get restaurant menu

### Orders
- `POST /orders` - Create new order (COD)
- `GET /orders/history` - Get user's order history

### AI Assistant
- `POST /ai/order-assistant` - AI chat endpoint
  - Request: `{ message: string, conversationHistory: array }`
  - Response: `{ message: string, suggestions?: array }`

## Pages

### 1. Login & Register
- JWT-based authentication
- Form validation
- Error handling

### 2. Home Page
- Restaurant listing with images
- Search functionality
- Filter by trending/top-rated
- Responsive grid layout

### 3. Restaurant Page
- Restaurant details
- Menu items by category
- Add to cart functionality
- Veg/Non-veg indicators

### 4. Cart Page
- View cart items
- Update quantities
- Remove items
- Price breakdown
- Proceed to checkout

### 5. Checkout Page
- Delivery address form
- Order summary
- COD payment only
- Form validation

### 6. Orders Page
- Order history
- Order status tracking
- Order details

### 7. AI Assistant Page
- Chat interface
- Natural language processing
- Smart food recommendations
- 3 suggestion types:
  - Best Price
  - Fastest Delivery
  - Top Rated
- Direct add to cart

## Mock Data

The app includes mock data for development when the backend is not available. This allows full frontend testing without a backend server.

## NLP Integration

The AI Assistant uses Natural Language Processing to:
- Understand user intent (food type, preferences)
- Extract entities (cuisines, restaurants, items)
- Provide contextual recommendations
- Maintain conversation flow

For production, integrate with:
- OpenAI GPT API
- Google Dialogflow
- Rasa NLP
- Custom NLP model

## Future Enhancements

🚀 **Phase 2 - Voice Assistant:**
- Speech-to-Text integration
- Voice commands
- Text-to-Speech responses
- Wake word detection

📱 **Additional Features:**
- Payment gateway integration
- Real-time order tracking
- Push notifications
- User reviews & ratings
- Favorites/Wishlists
- Restaurant owner dashboard

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

## Author

Built with ❤️ for the AI Food Ordering App
