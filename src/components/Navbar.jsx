import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { Home, ShoppingCart, Package, Bot, LogOut, User } from 'lucide-react';
import AddressPicker from './AddressPicker';
import AddressModal from './AddressModal';
import { addressAPI } from '../services/api';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { getTotalItems } = useCart();
  const location = useLocation();
  const navigate = useNavigate();
  const [showAddressModal, setShowAddressModal] = useState(false);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [editingAddress, setEditingAddress] = useState(null);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleAddressSelect = (address) => {
    setSelectedAddress(address);
    // Trigger restaurant refresh in Home component
    window.dispatchEvent(new CustomEvent('addressChanged', { detail: address }));
  };

  const handleAddNewAddress = () => {
    setEditingAddress(null);
    setShowAddressModal(true);
  };

  const handleEditAddress = (address) => {
    setEditingAddress(address);
    setShowAddressModal(true);
  };

  const handleSaveAddress = async (addressData) => {
    try {
      if (editingAddress) {
        // Update existing address
        await addressAPI.update(editingAddress.id, addressData);
      } else {
        // Create new address
        await addressAPI.create(addressData);
      }
      setShowAddressModal(false);
      setEditingAddress(null);
      // Trigger event to refresh address picker
      window.dispatchEvent(new Event('addressAdded'));
    } catch (error) {
      console.error('Full error details:', error);
      console.error('Error response:', error.response);
      console.error('Current token:', localStorage.getItem('token'));
      
      if (error.response?.status === 401) {
        // Session expired or invalid token - logout and redirect
        setShowAddressModal(false);
        setEditingAddress(null);
        const errorMsg = error.response?.data?.msg || error.response?.data?.error || 'Session expired';
        alert(`Authentication Error: ${errorMsg}\n\nToken in localStorage: ${localStorage.getItem('token')?.substring(0, 50)}...\n\nPlease try:\n1. Logout completely\n2. Close browser\n3. Login again`);
        logout();
        setTimeout(() => {
          navigate('/login');
        }, 100);
      } else {
        const errorMsg = error.response?.data?.error || error.message || 'Unknown error';
        alert(`Failed to save address: ${errorMsg}`);
      }
    }
  };

  const isActive = (path) => location.pathname === path;

  return (
    <>
      <nav className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <div className="bg-primary rounded-full p-2">
                <Home className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">AI FoodApp</span>
            </Link>

            {/* Address Picker - Centered */}
            <div className="hidden lg:flex flex-1 justify-center max-w-md mx-4">
              <AddressPicker 
                onAddressSelect={handleAddressSelect}
                onAddNewAddress={handleAddNewAddress}
                onEditAddress={handleEditAddress}
              />
            </div>

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

          {/* Mobile Address Picker */}
          <div className="lg:hidden pb-3">
            <AddressPicker 
              onAddressSelect={handleAddressSelect}
              onAddNewAddress={handleAddNewAddress}
              onEditAddress={handleEditAddress}
            />
          </div>
        </div>
      </nav>

      {/* Address Modal */}
      <AddressModal
        isOpen={showAddressModal}
        onClose={() => {
          setShowAddressModal(false);
          setEditingAddress(null);
        }}
        onSave={handleSaveAddress}
        editAddress={editingAddress}
      />
    </>
  );
};

export default Navbar;
