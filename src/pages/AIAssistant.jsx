import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { aiAPI } from '../services/api';
import Navbar from '../components/Navbar';
import { Send, Bot, User, Check } from 'lucide-react';

const AIAssistant = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI food assistant. Tell me what you'd like to eat, and I'll help you find the perfect meal! 🍕\n\nYou can also ask me to place orders directly! Just say something like:\n'Place order for Margherita Pizza from Pizza Palace with cash on delivery'",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
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

      // Check if order was placed successfully
      if (response.data.success && response.data.order) {
        const orderDetails = response.data.order_details;
        const botMessage = {
          id: messages.length + 2,
          text: response.data.message,
          sender: 'bot',
          timestamp: new Date(),
          orderPlaced: true,
          orderData: {
            orderId: response.data.order.id,
            dish: orderDetails.dish,
            restaurant: orderDetails.restaurant,
            price: orderDetails.price,
            paymentMethod: orderDetails.payment_method.replace('_', ' '),
            status: response.data.order.status
          }
        };
        setMessages(prev => [...prev, botMessage]);
      } 
      // Check for errors that need user action
      else if (response.data.error) {
        const needLogin = response.data.need_login;
        const botMessage = {
          id: messages.length + 2,
          text: response.data.error,
          sender: 'bot',
          timestamp: new Date(),
          needLogin: needLogin
        };
        setMessages(prev => [...prev, botMessage]);
      }
      // Regular AI response
      else if (response.data.response) {
        const botMessage = {
          id: messages.length + 2,
          text: response.data.response,
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('AI Assistant Error:', error);
      
      // Show error message to user
      const botMessage = {
        id: messages.length + 2,
        text: "Sorry, I'm having trouble connecting to the server. Please make sure you're logged in and try again. If the issue persists, try browsing restaurants directly from the home page.",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } finally {
      setLoading(false);
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
                    
                    {/* Login Prompt */}
                    {message.needLogin && (
                      <button
                        onClick={() => navigate('/login')}
                        className="mt-3 w-full bg-cherry text-white py-2 px-4 rounded-lg hover:bg-[#5A0A14] transition font-medium"
                      >
                        Login / Register
                      </button>
                    )}
                    
                    {/* Order Confirmation Card */}
                    {message.orderPlaced && message.orderData && (
                      <div className="mt-3 bg-white rounded-lg p-3 border-2 border-green-500">
                        <div className="flex items-center gap-2 mb-2">
                          <Check className="w-5 h-5 text-green-600" />
                          <span className="font-bold text-green-600">Order Placed!</span>
                        </div>
                        <div className="text-sm text-gray-700 space-y-1">
                          <p><strong>Order ID:</strong> #{message.orderData.orderId}</p>
                          <p><strong>Dish:</strong> {message.orderData.dish}</p>
                          <p><strong>Restaurant:</strong> {message.orderData.restaurant}</p>
                          <p><strong>Price:</strong> ₹{message.orderData.price}</p>
                          <p><strong>Payment:</strong> {message.orderData.paymentMethod}</p>
                          <p><strong>Status:</strong> <span className="capitalize">{message.orderData.status}</span></p>
                        </div>
                        <button
                          onClick={() => navigate('/orders')}
                          className="mt-2 w-full bg-cherry text-white py-1.5 px-3 rounded text-sm hover:bg-[#5A0A14] transition"
                        >
                          View Order Details
                        </button>
                      </div>
                    )}
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
                placeholder="Tell me what you want to eat or place an order..."
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
              Try: "Place order for Margherita Pizza from Pizza Palace with cash on delivery"
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
