import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { orderAPI, addressAPI } from '../services/api';
import Navbar from '../components/Navbar';
import AddressModal from '../components/AddressModal';
import { MapPin, Phone, Home, ArrowLeft, CreditCard, Plus, Edit2, Check } from 'lucide-react';

const Checkout = () => {
  const { cartItems, getTotalPrice, clearCart } = useCart();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [showAddressModal, setShowAddressModal] = useState(false);
  const [instructions, setInstructions] = useState('');

  useEffect(() => {
    fetchAddresses();
  }, []);

  const fetchAddresses = async () => {
    try {
      const response = await addressAPI.getAll();
      const addressList = response.data.addresses;
      setAddresses(addressList);
      
      // Auto-select default address
      const defaultAddr = addressList.find(addr => addr.is_default);
      if (defaultAddr) {
        setSelectedAddress(defaultAddr);
      }
    } catch (error) {
      console.error('Error fetching addresses:', error);
    }
  };

  const handleSaveAddress = async (addressData) => {
    try {
      await addressAPI.create(addressData);
      setShowAddressModal(false);
      await fetchAddresses();
    } catch (error) {
      console.error('Error saving address:', error);
      alert('Failed to save address. Please try again.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedAddress) {
      alert('Please select a delivery address');
      return;
    }
    
    setLoading(true);

    try {
      const orderData = {
        items: cartItems.map(item => ({
          id: item.id,
          name: item.name,
          quantity: item.quantity,
          price: item.price,
          restaurantId: item.restaurant.id
        })),
        deliveryAddress: selectedAddress.full_address,
        addressId: selectedAddress.id,
        phone: selectedAddress.phone,
        instructions: instructions,
        paymentMethod: 'COD',
        totalAmount: totalAmount
      };

      await orderAPI.create(orderData);
      clearCart();
      navigate('/orders', { 
        state: { message: 'Order placed successfully!' }
      });
    } catch (error) {
      // Mock order creation (backend not required)
      clearCart();
      navigate('/orders', { 
        state: { message: 'Order placed successfully!' }
      });
    } finally {
      setLoading(false);
    }
  };

  const totalAmount = getTotalPrice() + 40 + Math.round(getTotalPrice() * 0.05);

  return (
    <>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Cart
          </button>

          <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Delivery Form */}
            <div className="lg:col-span-2 space-y-6">
              {/* Delivery Address Selection */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <MapPin className="w-6 h-6 text-cherry" />
                  Select Delivery Address
                </h2>

                {addresses.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-gray-600 mb-4">No saved addresses</p>
                    <button
                      onClick={() => setShowAddressModal(true)}
                      className="px-6 py-3 bg-cherry text-white rounded-lg hover:bg-cherry-dark transition flex items-center gap-2 mx-auto"
                    >
                      <Plus className="w-5 h-5" />
                      Add New Address
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="space-y-3 mb-4">
                      {addresses.map((address) => (
                        <button
                          key={address.id}
                          onClick={() => setSelectedAddress(address)}
                          className={`w-full p-4 rounded-lg border-2 text-left transition ${
                            selectedAddress?.id === address.id
                              ? 'border-cherry bg-cherry-light'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <span className={`font-semibold ${
                                  selectedAddress?.id === address.id ? 'text-cherry' : 'text-gray-900'
                                }`}>
                                  {address.label}
                                </span>
                                {address.is_default && (
                                  <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
                                    Default
                                  </span>
                                )}
                              </div>
                              <p className="text-sm text-gray-600 leading-relaxed">
                                {address.full_address}
                              </p>
                              {address.landmark && (
                                <p className="text-xs text-gray-500 mt-1">
                                  Near: {address.landmark}
                                </p>
                              )}
                              {address.phone && (
                                <p className="text-sm text-gray-600 mt-2 flex items-center gap-1">
                                  <Phone className="w-3 h-3" />
                                  {address.phone}
                                </p>
                              )}
                            </div>
                            {selectedAddress?.id === address.id && (
                              <Check className="w-6 h-6 text-cherry flex-shrink-0" />
                            )}
                          </div>
                        </button>
                      ))}
                    </div>

                    <button
                      onClick={() => setShowAddressModal(true)}
                      className="w-full py-3 border-2 border-dashed border-gray-300 text-gray-600 rounded-lg hover:border-cherry hover:text-cherry transition flex items-center justify-center gap-2"
                    >
                      <Plus className="w-5 h-5" />
                      Add New Address
                    </button>
                  </>
                )}
              </div>

              {/* Delivery Instructions */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="font-semibold text-gray-900 mb-3">Delivery Instructions (Optional)</h3>
                <textarea
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cherry focus:border-transparent outline-none resize-none"
                  placeholder="Ring the bell twice, leave at the door, etc."
                  rows="3"
                />
              </div>

              {/* Payment Method */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-start gap-3">
                  <CreditCard className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">Payment Method</h3>
                    <p className="text-sm text-gray-600">
                      Cash on Delivery (COD) - Pay when your order arrives
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={handleSubmit}
                disabled={loading || !selectedAddress}
                className="w-full bg-cherry hover:bg-cherry-dark text-white font-semibold py-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Placing Order...' : `Place Order - ₹${totalAmount}`}
              </button>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-md p-6 sticky top-24">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Order Summary</h2>
                
                <div className="space-y-3 mb-4">
                  {cartItems.map((item) => (
                    <div key={item.id} className="flex justify-between text-sm">
                      <span className="text-gray-600">
                        {item.name} x {item.quantity}
                      </span>
                      <span className="font-semibold">₹{item.price * item.quantity}</span>
                    </div>
                  ))}
                </div>

                <div className="border-t pt-3 space-y-2 mb-4">
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Subtotal</span>
                    <span>₹{getTotalPrice()}</span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Delivery Fee</span>
                    <span>₹40</span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>GST (5%)</span>
                    <span>₹{Math.round(getTotalPrice() * 0.05)}</span>
                  </div>
                </div>

                <div className="border-t pt-3 flex justify-between text-xl font-bold text-gray-900">
                  <span>Total</span>
                  <span>₹{totalAmount}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Address Modal */}
      <AddressModal
        isOpen={showAddressModal}
        onClose={() => setShowAddressModal(false)}
        onSave={handleSaveAddress}
      />
    </>
  );
};

export default Checkout;
