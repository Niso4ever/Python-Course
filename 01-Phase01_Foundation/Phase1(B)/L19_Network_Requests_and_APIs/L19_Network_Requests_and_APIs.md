# Lesson 19: Network Requests and APIs (Talking to the Outside World)

If your Python script is a house, its variables are the furniture inside. But sometimes, your agent needs information that isn't in the house—like the current weather, the latest news, or the price of a stock. To get that, the agent has to make a "phone call" to the outside world.

An API (Application Programming Interface) is a special website designed specifically for computers to read, rather than humans. 

## 1. Making a GET Request (Asking for Information)
The most common way to make a phone call in Python is using the `requests` library.

> **Metaphor:** The coffee machine calling the local warehouse to ask how many beans are currently in stock.
> **Plain English:** We send a message to a URL asking for data, and the server replies with a JSON dictionary.

```python
import requests

# 1. The phone number we are calling
url = "https://api.github.com"

# 2. Making the call (GET means "please give me data")
response = requests.get(url)

# 3. Reading the answer
if response.status_code == 200:
    data = response.json()
    print("The agent successfully got the data!")
else:
    print(f"The call failed with error: {response.status_code}")
```
> This is the **[L19]** pattern — making an HTTP GET request.

## 2. API Keys and Headers (Proving Who You Are)
Many APIs (like OpenAI, Anthropic, or specialized weather APIs) won't pick up the phone unless you prove who you are. We do this by passing "Headers", which act like an ID badge presented during the phone call.

```python
import requests

url = "https://api.some-service.com/data"

# The ID badge
headers = {
    "Authorization": "Bearer YOUR_SECRET_API_KEY_HERE"
}

response = requests.get(url, headers=headers)
data = response.json()
```

## Why This Matters for Architecture
1. **Agent Tools:** When you build an AI that can "search the web" or "check my calendar", the LLM itself isn't doing the searching. The AI generates the *parameters*, and then *your Python code* makes a `requests.get()` call to Google or Google Calendar.
2. **Pipelines:** AI systems are often a pipeline of API calls. You might call one API to get text, send that text to the LLM API, and send the LLM's response to an email API. The `requests` library is the glue that connects these systems.

In the next lesson, we will learn how to build a physical user interface for our agents so that normal humans can interact with them easily.
