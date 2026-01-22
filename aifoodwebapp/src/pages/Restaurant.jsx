import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { restaurantAPI } from '../services/api';
import { useCart } from '../context/CartContext';
import Navbar from '../components/Navbar';
import { Star, Clock, DollarSign, Plus, Check, Search } from 'lucide-react';

const Restaurant = () => {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [addedItems, setAddedItems] = useState({});
  
  const { addToCart } = useCart();

  useEffect(() => {
    fetchRestaurantData();
  }, [id]);

  const fetchRestaurantData = async () => {
    try {
      setLoading(true);
      const [restaurantRes, menuRes] = await Promise.all([
        restaurantAPI.getById(id),
        restaurantAPI.getMenu(id)
      ]);
      setRestaurant(restaurantRes.data.restaurant || restaurantRes.data);
      setMenu(menuRes.data.menu_items || menuRes.data || []);
    } catch (error) {
      console.error('Error fetching restaurant data:', error);
      setRestaurant(null);
      setMenu([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (item) => {
    addToCart(item, {
      id: restaurant.id,
      name: restaurant.name
    });
    
    setAddedItems({ ...addedItems, [item.id]: true });
    setTimeout(() => {
      setAddedItems(prev => ({ ...prev, [item.id]: false }));
    }, 1000);
  };

  const categories = ['all', ...new Set(menu.map(item => item.category))];

  const filteredMenu = Array.isArray(menu) ? menu.filter(item => {
    const matchesSearch = item.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  }) : [];

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
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Restaurant Header */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8">
          <div className="relative h-64">
            <img
              src={restaurant?.image_url || restaurant?.image || "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800"}
              alt={restaurant?.name}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
              <h1 className="text-4xl font-bold mb-2">{restaurant?.name}</h1>
              <p className="text-lg">{restaurant?.cuisine_type || restaurant?.cuisine}</p>
            </div>
          </div>
          
          <div className="p-6">
            <div className="flex flex-wrap gap-6 text-sm">
              <div className="flex items-center gap-2">
                <Star className="w-5 h-5 text-green-600 fill-current" />
                <span className="font-semibold">{restaurant?.rating || 'N/A'}</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-gray-600" />
                <span>{restaurant?.delivery_time || restaurant?.deliveryTime || 'N/A'}</span>
              </div>
              <div className="flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-gray-600" />
                <span>{restaurant?.priceRange || '₹100-500'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Search and Categories */}
        <div className="mb-8 space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search menu items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none bg-white"
            />
          </div>

          <div className="flex gap-3 flex-wrap">
            {categories.map(category => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-full font-medium transition capitalize ${
                  selectedCategory === category
                    ? 'bg-cherry text-white'
                    : 'bg-white text-gray-700 hover:bg-oat'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Menu Items Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMenu.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition"
            >
              <div className="relative h-48">
                <img
                  src={item.image_url || item.image || "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300"}
                  alt={item.name}
                  className="w-full h-full object-cover"
                />
                <div className={`absolute top-3 left-3 px-2 py-1 rounded text-xs font-semibold ${
                  item.is_vegetarian || item.isVeg ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                }`}>
                  {item.is_vegetarian || item.isVeg ? '🟢 Veg' : '🔴 Non-Veg'}
                </div>
              </div>
              
              <div className="p-4">
                <h3 className="text-lg font-bold text-gray-900 mb-1">
                  {item.name}
                </h3>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                  {item.description}
                </p>
                
                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold text-gray-900">
                    ₹{item.price}
                  </span>
                  <button
                    onClick={() => handleAddToCart(item)}
                    className={`px-4 py-2 rounded-lg font-semibold transition flex items-center gap-2 ${
                      addedItems[item.id]
                        ? 'bg-olive text-white'
                        : 'bg-cherry hover:bg-[#5A0A14] text-white'
                    }`}
                  >
                    {addedItems[item.id] ? (
                      <>
                        <Check className="w-4 h-4" />
                        Added
                      </>
                    ) : (
                      <>
                        <Plus className="w-4 h-4" />
                        Add
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredMenu.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No items found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Restaurant;
