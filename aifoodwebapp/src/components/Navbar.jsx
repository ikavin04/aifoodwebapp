import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { Home, ShoppingCart, Package, Bot, LogOut, User } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { getTotalItems } = useCart();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-primary rounded-full p-2">
              <Home className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">AI FoodApp</span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link
              to="/"
              className={`flex items-center space-x-1 ${
                isActive('/') ? 'text-cherry' : 'text-gray-600 hover:text-cherry'
              } transition`}
            >
              <Home className="w-5 h-5" />
              <span className="hidden sm:inline">Home</span>
            </Link>

            <Link
              to="/ai-assistant"
              className={`flex items-center space-x-1 ${
                isActive('/ai-assistant') ? 'text-cherry' : 'text-gray-600 hover:text-cherry'
              } transition`}
            >
              <Bot className="w-5 h-5" />
              <span className="hidden sm:inline">AI Assistant</span>
            </Link>

            <Link
              to="/cart"
              className={`flex items-center space-x-1 relative ${
                isActive('/cart') ? 'text-cherry' : 'text-gray-600 hover:text-cherry'
              } transition`}
            >
              <ShoppingCart className="w-5 h-5" />
              <span className="hidden sm:inline">Cart</span>
              {getTotalItems() > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {getTotalItems()}
                </span>
              )}
            </Link>

            <Link
              to="/orders"
              className={`flex items-center space-x-1 ${
                isActive('/orders') ? 'text-cherry' : 'text-gray-600 hover:text-cherry'
              } transition`}
            >
              <Package className="w-5 h-5" />
              <span className="hidden sm:inline">Orders</span>
            </Link>

            <div className="flex items-center space-x-3 pl-3 border-l border-gray-300">
              <div className="flex items-center space-x-2">
                <User className="w-5 h-5 text-gray-600" />
                <span className="hidden sm:inline text-sm text-gray-700">{user?.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 text-red-600 hover:text-red-700 transition"
              >
                <LogOut className="w-5 h-5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
