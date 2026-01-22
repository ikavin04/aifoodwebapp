import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { orderAPI } from '../services/api';
import Navbar from '../components/Navbar';
import { Package, Clock, CheckCircle, XCircle } from 'lucide-react';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await orderAPI.getHistory();
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
      // Mock data
      setOrders([
        {
          id: 'ORD001',
          items: [
            { name: 'Margherita Pizza', quantity: 2, price: 299 },
            { name: 'Garlic Bread', quantity: 1, price: 99 }
          ],
          restaurant: 'Pizza Palace',
          totalAmount: 737,
          status: 'delivered',
          paymentMethod: 'COD',
          orderDate: '2026-01-20T14:30:00',
          deliveryAddress: '123 Food Street, City Center, Mumbai - 400001'
        },
        {
          id: 'ORD002',
          items: [
            { name: 'BBQ Chicken Pizza', quantity: 1, price: 449 },
            { name: 'Caesar Salad', quantity: 1, price: 199 }
          ],
          restaurant: 'Pizza Palace',
          totalAmount: 688,
          status: 'in-progress',
          paymentMethod: 'COD',
          orderDate: '2026-01-22T10:15:00',
          deliveryAddress: '123 Food Street, City Center, Mumbai - 400001'
        },
        {
          id: 'ORD003',
          items: [
            { name: 'Chicken Biryani', quantity: 2, price: 350 }
          ],
          restaurant: 'Biryani House',
          totalAmount: 740,
          status: 'cancelled',
          paymentMethod: 'COD',
          orderDate: '2026-01-19T19:45:00',
          deliveryAddress: '123 Food Street, City Center, Mumbai - 400001'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'delivered':
        return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'in-progress':
        return <Clock className="w-6 h-6 text-blue-500" />;
      case 'cancelled':
        return <XCircle className="w-6 h-6 text-red-500" />;
      default:
        return <Package className="w-6 h-6 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'in-progress':
        return 'bg-blue-100 text-blue-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-96">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My Orders</h1>
        <p className="text-gray-600 mb-8">View your order history and track current orders</p>

        {location.state?.message && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6 flex items-center gap-2">
            <CheckCircle className="w-5 h-5" />
            {location.state.message}
          </div>
        )}

        {orders.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl shadow-md">
            <Package className="w-24 h-24 text-gray-300 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No orders yet</h2>
            <p className="text-gray-600">Start ordering to see your order history!</p>
          </div>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => (
              <div key={order.id} className="bg-white rounded-xl shadow-md overflow-hidden">
                <div className="p-6">
                  {/* Order Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-start gap-3">
                      {getStatusIcon(order.status)}
                      <div>
                        <h3 className="text-xl font-bold text-gray-900">
                          Order #{order.id}
                        </h3>
                        <p className="text-sm text-gray-600">{order.restaurant}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {formatDate(order.orderDate)}
                        </p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold capitalize ${getStatusColor(order.status)}`}>
                      {order.status.replace('-', ' ')}
                    </span>
                  </div>

                  {/* Order Items */}
                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    {order.items.map((item, index) => (
                      <div key={index} className="flex justify-between items-center py-2">
                        <span className="text-gray-700">
                          {item.name} <span className="text-gray-500">x {item.quantity}</span>
                        </span>
                        <span className="font-semibold text-gray-900">
                          ₹{item.price * item.quantity}
                        </span>
                      </div>
                    ))}
                  </div>

                  {/* Order Footer */}
                  <div className="flex items-center justify-between pt-4 border-t">
                    <div className="text-sm text-gray-600">
                      <p>Payment: <span className="font-semibold">{order.paymentMethod}</span></p>
                      <p className="mt-1">Delivery: {order.deliveryAddress}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Total Amount</p>
                      <p className="text-2xl font-bold text-gray-900">₹{order.totalAmount}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Orders;
