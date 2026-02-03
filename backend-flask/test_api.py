import requests
import json

# Test login
print("Testing login...")
login_response = requests.post('http://localhost:5000/auth/login', 
    json={'email': 'test@example.com', 'password': 'password123'})

print(f"Login Status: {login_response.status_code}")
print(f"Login Response: {login_response.json()}")

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"\nToken: {token[:50]}...")
    
    # Test address endpoint with token
    print("\n\nTesting address endpoint...")
    headers = {'Authorization': f'Bearer {token}'}
    address_response = requests.get('http://localhost:5000/addresses', headers=headers)
    
    print(f"Address Status: {address_response.status_code}")
    print(f"Address Response: {address_response.text}")
    
    if address_response.status_code != 200:
        print("\nERROR: Address endpoint failed!")
    else:
        print("\nSUCCESS: Address endpoint working!")
