"""Input validation utilities"""
import re


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_register(data):
    """Validate registration data"""
    errors = []
    
    if not data:
        return False, ['No data provided']
    
    # Check required fields
    if not data.get('name'):
        errors.append('Name is required')
    elif len(data.get('name', '')) < 2:
        errors.append('Name must be at least 2 characters')
    
    if not data.get('email'):
        errors.append('Email is required')
    elif not validate_email(data.get('email', '')):
        errors.append('Invalid email format')
    
    if not data.get('password'):
        errors.append('Password is required')
    elif len(data.get('password', '')) < 6:
        errors.append('Password must be at least 6 characters')
    
    return len(errors) == 0, errors


def validate_login(data):
    """Validate login data"""
    errors = []
    
    if not data:
        return False, ['No data provided']
    
    if not data.get('email'):
        errors.append('Email is required')
    
    if not data.get('password'):
        errors.append('Password is required')
    
    return len(errors) == 0, errors


def validate_cart_item(data):
    """Validate cart item data"""
    errors = []
    
    if not data:
        return False, ['No data provided']
    
    if not data.get('menu_item_id'):
        errors.append('Menu item ID is required')
    
    quantity = data.get('quantity', 1)
    if not isinstance(quantity, int) or quantity < 1:
        errors.append('Quantity must be a positive integer')
    
    return len(errors) == 0, errors


def validate_order(data):
    """Validate order data"""
    errors = []
    
    if not data:
        return False, ['No data provided']
    
    if not data.get('items') or not isinstance(data.get('items'), list):
        errors.append('Items array is required')
    elif len(data.get('items', [])) == 0:
        errors.append('Order must contain at least one item')
    
    if not data.get('delivery_address'):
        errors.append('Delivery address is required')
    
    if not data.get('phone'):
        errors.append('Phone number is required')
    
    # Validate each item
    for i, item in enumerate(data.get('items', [])):
        if not item.get('menu_item_id'):
            errors.append(f'Item {i + 1}: Menu item ID is required')
        
        quantity = item.get('quantity', 1)
        if not isinstance(quantity, int) or quantity < 1:
            errors.append(f'Item {i + 1}: Quantity must be a positive integer')
    
    return len(errors) == 0, errors
