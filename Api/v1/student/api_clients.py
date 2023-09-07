import requests

url = "YOUR_API_ENDPOINT"  # Replace with the actual API endpoint
jwt_token = "YOUR_JWT_TOKEN"  # Replace with your valid JWT token

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json",  # Adjust content type if necessary
}

response = requests.get(url, headers=headers)