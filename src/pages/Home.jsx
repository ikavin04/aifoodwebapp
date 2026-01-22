import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { restaurantAPI } from '../services/api';
import Navbar from '../components/Navbar';
import { Search, Star, Clock, DollarSign, TrendingUp } from 'lucide-react';

const Home = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    try {
      setLoading(true);
      const response = await restaurantAPI.getAll();
      setRestaurants(response.data);
    } catch (error) {
      console.error('Error fetching restaurants:', error);
      // Mock data for development
      setRestaurants([
        {
          id: 1,
          name: "Pizza Palace",
          cuisine: "Italian",
          rating: 4.5,
          deliveryTime: "30-35 min",
          priceRange: "₹200-400",
          image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400",
          trending: true
        },
        {
          id: 2,
          name: "Burger King",
          cuisine: "American",
          rating: 4.2,
          deliveryTime: "25-30 min",
          priceRange: "₹150-300",
          image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
          trending: false
        },
        {
          id: 3,
          name: "Biryani House",
          cuisine: "Indian",
          rating: 4.7,
          deliveryTime: "40-45 min",
          priceRange: "₹250-500",
          image: "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400",
          trending: true
        },
        {
          id: 4,
          name: "Sushi Bar",
          cuisine: "Japanese",
          rating: 4.4,
          deliveryTime: "35-40 min",
          priceRange: "₹400-800",
          image: "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400",
          trending: false
        },
        {
          id: 5,
          name: "Taco Fiesta",
          cuisine: "Mexican",
          rating: 4.3,
          deliveryTime: "30-35 min",
          priceRange: "₹200-350",
          image: "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400",
          trending: true
        },
        {
          id: 6,
          name: "Thai Express",
          cuisine: "Thai",
          rating: 4.6,
          deliveryTime: "35-40 min",
          priceRange: "₹300-600",
          image: "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400",
          trending: false
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const filteredRestaurants = restaurants.filter(restaurant => {
    const matchesSearch = restaurant.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         restaurant.cuisine.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (filterType === 'trending') return matchesSearch && restaurant.trending;
    if (filterType === 'rating') return matchesSearch && restaurant.rating >= 4.5;
    return matchesSearch;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Order Food Online
          </h1>
          <p className="text-gray-600">Discover the best food & drinks in your area</p>
        </div>

        {/* Search and Filter */}
        <div className="mb-8 space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search for restaurants or cuisines..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
            />
          </div>

          <div className="flex gap-3 flex-wrap">
            <button
              onClick={() => setFilterType('all')}
              className={`px-4 py-2 rounded-full font-medium transition ${
                filterType === 'all'
                  ? 'bg-primary text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              All Restaurants
            </button>
            <button
              onClick={() => setFilterType('trending')}
              className={`px-4 py-2 rounded-full font-medium transition flex items-center gap-1 ${
                filterType === 'trending'
                  ? 'bg-primary text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              Trending
            </button>
            <button
              onClick={() => setFilterType('rating')}
              className={`px-4 py-2 rounded-full font-medium transition flex items-center gap-1 ${
                filterType === 'rating'
                  ? 'bg-primary text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Star className="w-4 h-4" />
              Top Rated
            </button>
          </div>
        </div>

        {/* Restaurant Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="spinner"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredRestaurants.map((restaurant) => (
              <Link
                key={restaurant.id}
                to={`/restaurant/${restaurant.id}`}
                className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition duration-300 transform hover:-translate-y-1"
              >
                <div className="relative h-48">
                  <img
                    src={restaurant.image}
                    alt={restaurant.name}
                    className="w-full h-full object-cover"
                  />
                  {restaurant.trending && (
                    <div className="absolute top-3 left-3 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      Trending
                    </div>
                  )}
                </div>
                
                <div className="p-4">
                  <h3 className="text-xl font-bold text-gray-900 mb-1">
                    {restaurant.name}
                  </h3>
                  <p className="text-gray-600 text-sm mb-3">{restaurant.cuisine}</p>
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-1 text-green-600 font-semibold">
                      <Star className="w-4 h-4 fill-current" />
                      {restaurant.rating}
                    </div>
                    <div className="flex items-center gap-1 text-gray-600">
                      <Clock className="w-4 h-4" />
                      {restaurant.deliveryTime}
                    </div>
                    <div className="flex items-center gap-1 text-gray-600">
                      <DollarSign className="w-4 h-4" />
                      {restaurant.priceRange}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {filteredRestaurants.length === 0 && !loading && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No restaurants found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
