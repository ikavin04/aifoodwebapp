import React, { createContext, useState, useContext, useEffect } from 'react';
import { cartAPI } from '../services/api';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Load cart from database on mount
  useEffect(() => {
    loadCartFromDatabase();
  }, []);

  const loadCartFromDatabase = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        // If not logged in, load from localStorage as fallback
        const savedCart = localStorage.getItem('cart');
        if (savedCart) {
          setCartItems(JSON.parse(savedCart));
        }
        return;
      }

      const response = await cartAPI.getCart();
      if (response.data && response.data.cart_items) {
        setCartItems(response.data.cart_items);
      }
    } catch (error) {
      // Fallback to localStorage if database fails
      console.error('Failed to load cart from database:', error);
      const savedCart = localStorage.getItem('cart');
      if (savedCart) {
        setCartItems(JSON.parse(savedCart));
      }
    }
  };

  const addToCart = async (item, restaurant) => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (token) {
        // Add to database
        const response = await cartAPI.addItem({
          menu_item_id: item.id,
          quantity: 1
        });
        
        // Reload cart from database to get updated state
        await loadCartFromDatabase();
      } else {
        // Fallback to localStorage
        setCartItems(prevItems => {
          const existingItem = prevItems.find(i => i.menu_item?.id === item.id || i.id === item.id);
          
          let newItems;
          if (existingItem) {
            newItems = prevItems.map(i =>
              (i.menu_item?.id === item.id || i.id === item.id) 
                ? { ...i, quantity: i.quantity + 1 } 
                : i
            );
          } else {
            newItems = [...prevItems, { menu_item: item, quantity: 1, restaurant }];
          }
          
          localStorage.setItem('cart', JSON.stringify(newItems));
          return newItems;
        });
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      // Fallback to localStorage on error
      setCartItems(prevItems => {
        const existingItem = prevItems.find(i => i.menu_item?.id === item.id || i.id === item.id);
        
        let newItems;
        if (existingItem) {
          newItems = prevItems.map(i =>
            (i.menu_item?.id === item.id || i.id === item.id) 
              ? { ...i, quantity: i.quantity + 1 } 
              : i
          );
        } else {
          newItems = [...prevItems, { menu_item: item, quantity: 1, restaurant }];
        }
        
        localStorage.setItem('cart', JSON.stringify(newItems));
        return newItems;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const removeFromCart = async (itemId) => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (token) {
        await cartAPI.removeItem(itemId);
        await loadCartFromDatabase();
      } else {
        setCartItems(prevItems => {
          const newItems = prevItems.filter(item => item.id !== itemId);
          localStorage.setItem('cart', JSON.stringify(newItems));
          return newItems;
        });
      }
    } catch (error) {
      console.error('Error removing from cart:', error);
      // Fallback to localStorage
      setCartItems(prevItems => {
        const newItems = prevItems.filter(item => item.id !== itemId);
        localStorage.setItem('cart', JSON.stringify(newItems));
        return newItems;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId);
      return;
    }
    
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (token) {
        await cartAPI.updateItem(itemId, { quantity });
        await loadCartFromDatabase();
      } else {
        setCartItems(prevItems => {
          const newItems = prevItems.map(item =>
            item.id === itemId ? { ...item, quantity } : item
          );
          localStorage.setItem('cart', JSON.stringify(newItems));
          return newItems;
        });
      }
    } catch (error) {
      console.error('Error updating cart quantity:', error);
      // Fallback to localStorage
      setCartItems(prevItems => {
        const newItems = prevItems.map(item =>
          item.id === itemId ? { ...item, quantity } : item
        );
        localStorage.setItem('cart', JSON.stringify(newItems));
        return newItems;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const clearCart = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (token) {
        await cartAPI.clearCart();
        setCartItems([]);
      } else {
        setCartItems([]);
        localStorage.removeItem('cart');
      }
    } catch (error) {
      console.error('Error clearing cart:', error);
      // Clear locally anyway
      setCartItems([]);
      localStorage.removeItem('cart');
    } finally {
      setIsLoading(false);
    }
  };

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => {
      const price = item.menu_item?.price || item.price || 0;
      return total + (price * item.quantity);
    }, 0);
  };

  const getTotalItems = () => {
    return cartItems.reduce((total, item) => total + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      cartItems,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getTotalPrice,
      getTotalItems,
      isLoading,
      refreshCart: loadCartFromDatabase
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};
