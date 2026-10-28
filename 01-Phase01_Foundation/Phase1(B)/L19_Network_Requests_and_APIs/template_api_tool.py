"""
TEMPLATE: API Request Tool
CURRICULUM PATTERN: L19
DESCRIPTION: A standalone tool that makes a real network request.
This is the pattern used when giving an LLM the ability to "browse the web" 
or look up live information explicitly.
"""

import requests

def get_joke(topic=""):
    """
    Pattern [L19] - An agent tool that makes an API call.
    Fetches a random joke from an external public API based on a topic.
    """
    print(f"🔧 Tool Execution: Fetching a joke about '{topic}'...")
    
    url = "https://v2.jokeapi.dev/joke/Any"
    
    # We pass query parameters using a dictionary securely
    params = {
        "safe-mode": "true",
        "type": "single",
        "contains": topic
    }
    
    try:
        # 1. Make the phone call
        response = requests.get(url, params=params)
        
        # 2. Did they pick up?
        if response.status_code == 200:
            data = response.json()
            
            # The API returns an "error" key if the topic wasn't found
            if data.get("error") == True:
                return f"Could not find a friendly joke about {topic}."
                
            return data["joke"]
            
        else:
            return f"API Error: Received status code {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        # This catches network errors (e.g., your laptop has no Wi-Fi)
        return f"Network Error: Could not connect to the joke API. Details: {e}"

# ==========================================
# USAGE
# ==========================================
if __name__ == "__main__":
    # Test the tool directly
    print("Result:", get_joke("computer"))
