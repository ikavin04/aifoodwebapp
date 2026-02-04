import React, { useState, useEffect, useRef } from 'react';
import { MapPin, ChevronDown, Plus, Edit2, Trash2, Check } from 'lucide-react';
import { addressAPI } from '../services/api';

const AddressPicker = ({ onAddressSelect, onAddNewAddress, onEditAddress }) => {
  const [addresses, setAddresses] = useState([]);
  const [currentAddress, setCurrentAddress] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const dropdownRef = useRef(null);

  useEffect(() => {
    // Only fetch if user has a token
    const token = localStorage.getItem('token');
    if (token) {
      fetchAddresses();
    } else {
      setLoading(false);
    }

    // Listen for address changes or additions
    const handleAddressUpdate = () => {
      const token = localStorage.getItem('token');
      if (token) {
        fetchAddresses();
      }
    };

    window.addEventListener('addressChanged', handleAddressUpdate);
    window.addEventListener('addressAdded', handleAddressUpdate);

    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    
    return () => {
      window.removeEventListener('addressChanged', handleAddressUpdate);
      window.removeEventListener('addressAdded', handleAddressUpdate);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const fetchAddresses = async () => {
    try {
      setLoading(true);
      const response = await addressAPI.getAll();
      const addressList = response.data.addresses;
      setAddresses(addressList);
      
      // Set current address (default or first)
      const defaultAddr = addressList.find(addr => addr.is_default) || addressList[0];
      if (defaultAddr) {
        setCurrentAddress(defaultAddr);
      }
    } catch (error) {
      // Silently handle if not authenticated
      if (error.response?.status !== 401) {
        console.error('Error fetching addresses:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAddress = async (address) => {
    try {
      await addressAPI.setCurrent(address.id);
      setCurrentAddress(address);
      setIsOpen(false);
      if (onAddressSelect) {
        onAddressSelect(address);
      }
    } catch (error) {
      console.error('Error setting current address:', error);
    }
  };

  const handleDeleteAddress = async (e, addressId) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this address?')) {
      try {
        await addressAPI.delete(addressId);
        await fetchAddresses();
      } catch (error) {
        console.error('Error deleting address:', error);
      }
    }
  };

  const handleEditAddress = (e, address) => {
    e.stopPropagation();
    setIsOpen(false);
    if (onEditAddress) {
      onEditAddress(address);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg animate-pulse">
        <MapPin className="w-4 h-4 text-gray-400" />
        <span className="text-sm text-gray-400">Loading...</span>
      </div>
    );
  }

  if (addresses.length === 0) {
    return (
      <button
        onClick={() => onAddNewAddress && onAddNewAddress()}
        className="flex items-center gap-2 px-3 py-2 bg-cherry-light text-cherry rounded-lg hover:bg-cherry hover:text-white transition"
      >
        <MapPin className="w-4 h-4" />
        <span className="text-sm font-medium">Add Address</span>
      </button>
    );
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 bg-white border-2 border-gray-200 rounded-lg hover:border-cherry transition max-w-xs"
      >
        <MapPin className="w-4 h-4 text-cherry flex-shrink-0" />
        <div className="flex flex-col items-start min-w-0 flex-1">
          <span className="text-xs text-gray-500 font-medium">{currentAddress?.label || 'Select Address'}</span>
          <span className="text-sm text-gray-900 truncate w-full">
            {currentAddress ? `${currentAddress.city}, ${currentAddress.state}` : 'No address selected'}
          </span>
        </div>
        <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform flex-shrink-0 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-96 bg-white rounded-lg shadow-2xl border border-gray-200 z-50 max-h-96 overflow-y-auto">
          <div className="p-3 border-b border-gray-200 bg-gray-50">
            <h3 className="font-semibold text-gray-900">Select Delivery Address</h3>
          </div>
          
          <div className="p-2">
            {addresses.map((address) => (
              <button
                key={address.id}
                onClick={() => handleSelectAddress(address)}
                className={`w-full p-3 rounded-lg mb-2 text-left transition group relative ${
                  currentAddress?.id === address.id
                    ? 'bg-cherry-light border-2 border-cherry'
                    : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`font-semibold text-sm ${
                        currentAddress?.id === address.id ? 'text-cherry' : 'text-gray-900'
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
                      {address.address_line1}, {address.address_line2 && `${address.address_line2}, `}
                      {address.city}, {address.state} - {address.pincode}
                    </p>
                    {address.landmark && (
                      <p className="text-xs text-gray-500 mt-1">
                        Near: {address.landmark}
                      </p>
                    )}
                  </div>
                  
                  {currentAddress?.id === address.id && (
                    <Check className="w-5 h-5 text-cherry flex-shrink-0" />
                  )}
                </div>

                <div className="flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <div
                    onClick={(e) => handleEditAddress(e, address)}
                    className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
                  >
                    <Edit2 className="w-3 h-3" />
                    Edit
                  </div>
                  <div
                    onClick={(e) => handleDeleteAddress(e, address.id)}
                    className="text-xs text-red-600 hover:text-red-700 flex items-center gap-1 cursor-pointer"
                  >
                    <Trash2 className="w-3 h-3" />
                    Delete
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="p-3 border-t border-gray-200">
            <button
              onClick={() => {
                setIsOpen(false);
                onAddNewAddress && onAddNewAddress();
              }}
              className="w-full py-2 px-4 bg-cherry text-white rounded-lg hover:bg-cherry-dark transition flex items-center justify-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Add New Address
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AddressPicker;
