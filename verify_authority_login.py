import requests
import json

def test_authority_login():
    url = "http://localhost:8000/api/auth/login"
    payload = {
        "email": "admin@city.gov",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Login Successful!")
            print(f"Access Token: {data.get('access_token')[:20]}...")
            print(f"Role: {data.get('role')}")
            print(f"Email: {data.get('email')}")
            
            # Verify role is authority
            assert data.get('role') == 'authority', f"Expected role 'authority', got '{data.get('role')}'"
            assert data.get('email') == 'admin@city.gov', f"Expected email 'admin@city.gov', got '{data.get('email')}'"
            return True
        else:
            print("Login Failed!")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    test_authority_login()
