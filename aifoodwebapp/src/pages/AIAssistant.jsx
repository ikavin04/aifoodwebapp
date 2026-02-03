import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { aiAPI } from '../services/api';
import { useCart } from '../context/CartContext';
import Navbar from '../components/Navbar';
import { Send, Bot, User, TrendingUp, Clock, Star, Check } from 'lucide-react';

const AIAssistant = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI food assistant. Tell me what you'd like to eat, and I'll help you find the perfect meal! 🍕",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(null);
  const messagesEndRef = useRef(null);
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: input,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await aiAPI.chat({
        message: input,
        conversationHistory: messages
      });

      const botMessage = {
        id: messages.length + 2,
        text: response.data.message,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);

      // If AI provides suggestions, auto-add first one to cart
      if (response.data.suggestions && response.data.suggestions.length > 0) {
        handleConfirmOrder(response.data.suggestions[0]);
      }
    } catch (error) {
      // Using mock AI responses (backend not required)
      
      // Mock AI response
      const mockResponse = generateMockResponse(input);
      const botMessage = {
        id: messages.length + 2,
        text: mockResponse.message,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      
      if (mockResponse.suggestions && mockResponse.suggestions.length > 0) {
        handleConfirmOrder(mockResponse.suggestions[0]);
      }
    } finally {
      setLoading(false);
    }
  };

  const generateMockResponse = (userInput) => {
    const input = userInput.toLowerCase();
    
    if (input.includes('pizza') || input.includes('italian')) {
      return {
        message: "Great choice! I found some amazing pizza options for you. Here are my top 3 recommendations based on price, delivery time, and ratings:",
        suggestions: [
          {
            id: 1,
            restaurant: 'Pizza Palace',
            items: ['Margherita Pizza', 'Garlic Bread'],
            totalPrice: 398,
            deliveryTime: '30 min',
            rating: 4.5,
            type: 'cheapest',
            restaurantId: 1
          },
          {
            id: 2,
            restaurant: 'Pizza Express',
            items: ['Pepperoni Pizza'],
            totalPrice: 399,
            deliveryTime: '20 min',
            rating: 4.3,
            type: 'fastest',
            restaurantId: 1
          },
          {
            id: 3,
            restaurant: 'Pizza Palace',
            items: ['BBQ Chicken Pizza', 'Caesar Salad'],
            totalPrice: 648,
            deliveryTime: '35 min',
            rating: 4.7,
            type: 'best-rated',
            restaurantId: 1
          }
        ]
      };
    } else if (input.includes('biryani') || input.includes('indian')) {
      return {
        message: "Excellent! I've found some delicious biryani options. Here are my recommendations:",
        suggestions: [
          {
            id: 1,
            restaurant: 'Biryani House',
            items: ['Chicken Biryani', 'Raita'],
            totalPrice: 320,
            deliveryTime: '40 min',
            rating: 4.7,
            type: 'cheapest',
            restaurantId: 3
          },
          {
            id: 2,
            restaurant: 'Quick Biryani',
            items: ['Veg Biryani'],
            totalPrice: 250,
            deliveryTime: '25 min',
            rating: 4.2,
            type: 'fastest',
            restaurantId: 3
          },
          {
            id: 3,
            restaurant: 'Biryani House',
            items: ['Mutton Biryani', 'Kebab'],
            totalPrice: 550,
            deliveryTime: '45 min',
            rating: 4.8,
            type: 'best-rated',
            restaurantId: 3
          }
        ]
      };
    } else {
      return {
        message: "I'd love to help you find the perfect meal! Could you tell me what type of cuisine you're craving? For example: pizza, biryani, burger, sushi, tacos, or anything else!",
        suggestions: null
      };
    }
  };

  const handleConfirmOrder = (suggestion) => {
    // Add items to cart
    suggestion.items.forEach((itemName, index) => {
      const mockItem = {
        id: Date.now() + index,
        name: itemName,
        price: Math.round(suggestion.totalPrice / suggestion.items.length),
        description: `Delicious ${itemName} from ${suggestion.restaurant}`,
        image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300',
        category: 'Main Course',
        isVeg: itemName.toLowerCase().includes('veg')
      };
      
      addToCart(mockItem, {
        id: suggestion.restaurantId,
        name: suggestion.restaurant
      });
    });

    // Show success message
    const botMessage = {
      id: messages.length + 1,
      text: `Great! I've added ${suggestion.items.join(', ')} to your cart. You can proceed to checkout or continue browsing.`,
      sender: 'bot',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, botMessage]);
    setSuggestions(null);
  };

  const getSuggestionIcon = (type) => {
    switch (type) {
      case 'cheapest':
        return <TrendingUp className="w-5 h-5 text-green-600" />;
      case 'fastest':
        return <Clock className="w-5 h-5 text-blue-600" />;
      case 'best-rated':
        return <Star className="w-5 h-5 text-yellow-600 fill-current" />;
      default:
        return null;
    }
  };

  const getSuggestionLabel = (type) => {
    switch (type) {
      case 'cheapest':
        return 'Best Price';
      case 'fastest':
        return 'Fastest Delivery';
      case 'best-rated':
        return 'Top Rated';
      default:
        return '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-gradient-to-r from-cherry to-olive rounded-xl p-6 mb-6 text-white">
          <h1 className="text-3xl font-bold mb-2">AI Food Assistant</h1>
          <p className="text-butter">
            Just tell me what you're craving, and I'll find the best options for you!
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Chat Messages */}
          <div className="h-[500px] overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.sender === 'bot' && (
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-cherry flex items-center justify-center">
                      <Bot className="w-6 h-6 text-white" />
                    </div>
                  </div>
                )}
                
                <div className={`max-w-[70%] ${message.sender === 'user' ? 'order-2' : ''}`}>
                  <div
                    className={`rounded-2xl px-4 py-3 ${
                      message.sender === 'user'
                        ? 'bg-cherry text-white'
                        : 'bg-oat text-gray-900'
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.text}</p>
                  </div>
                  <p className="text-xs text-gray-500 mt-1 px-2">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>

                {message.sender === 'user' && (
                  <div className="flex-shrink-0 order-3">
                    <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
                      <User className="w-6 h-6 text-gray-600" />
                    </div>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-full bg-cherry flex items-center justify-center">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <div className="bg-oat rounded-2xl px-4 py-3">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}

            {/* Suggestions */}
            {suggestions && (
              <div className="space-y-3">
                {suggestions.map((suggestion) => (
                  <div
                    key={suggestion.id}
                    className="bg-gradient-to-r from-butter to-oat border border-[#E5D5B7] rounded-xl p-4 hover:shadow-md transition"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        {getSuggestionIcon(suggestion.type)}
                        <span className="font-bold text-gray-900 text-lg">
                          {getSuggestionLabel(suggestion.type)}
                        </span>
                      </div>
                      <span className="text-2xl font-bold text-cherry">
                        ₹{suggestion.totalPrice}
                      </span>
                    </div>

                    <div className="space-y-2 mb-3">
                      <p className="font-semibold text-gray-900">{suggestion.restaurant}</p>
                      <p className="text-sm text-gray-600">
                        {suggestion.items.join(' • ')}
                      </p>
                      <div className="flex gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {suggestion.deliveryTime}
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 text-yellow-500 fill-current" />
                          {suggestion.rating}
                        </div>
                      </div>
                    </div>

                    <button
                      onClick={() => handleConfirmOrder(suggestion)}
                      className="w-full bg-cherry hover:bg-[#5A0A14] text-white font-semibold py-2 px-4 rounded-lg transition flex items-center justify-center gap-2"
                    >
                      <Check className="w-5 h-5" />
                      Add to Cart
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t p-4 bg-gray-50">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Tell me what you want to eat..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="bg-cherry hover:bg-[#5A0A14] text-white p-3 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-6 h-6" />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Try: "I want pizza", "Show me biryani options", "Something quick and cheap"
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
