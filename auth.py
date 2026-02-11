import requests

def verify_credentials(email, password):
    auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'
    credentials = {'email': email, 'password': password}

    try:
        response = requests.post(auth_url, json=credentials, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # The server returns ["Verified", "True"] on success
            if len(result) >= 2 and result[0] == "Verified" and result[1] == "True":
                return True
        return False
    except Exception:
        return False