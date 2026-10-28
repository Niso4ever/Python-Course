"""
CHEATSHEET L19: Network Requests and APIs
Concepts: requests, GET, POST, JSON parsing, Headers
"""
import requests

# ==========================================
# PATTERN 1: Basic GET Request
# ==========================================
response = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")

# Always check if the request was successful (200 OK)
if response.status_code == 200:
    # Convert the JSON response into a Python dictionary
    data = response.json()
    print("Found Pokémon:", data["name"])
else:
    print("Error:", response.status_code)

# ==========================================
# PATTERN 2: GET with Parameters (?query=val)
# ==========================================
url = "https://api.nationalize.io/"
params = {
    "name": "michael"
}
# This automatically builds: https://api.nationalize.io/?name=michael
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Predicted nationalities:", response.json()["country"])

# ==========================================
# PATTERN 3: POST Request with Headers and JSON Body
# ==========================================
# This pattern is exactly how you call LLMs behind the scenes!
url = "https://httpbin.org/post"

headers = {
    "Authorization": "Bearer fake-api-key-123",
    "Content-Type": "application/json"
}

# The data we are sending TO the server
payload = {
    "message": "Hello server!"
}

# Note we use requests.post() instead of .get(), and pass json=payload
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("Successfully sent data to the server.")
