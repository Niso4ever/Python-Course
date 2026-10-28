# 3-Pass Reading: Network Requests and APIs

## Pass 1: Recognition (Labeling the Logic)

Look at `template_api_tool.py`. What building blocks do we see?

1. `import requests`
   - **Pattern:** `[L08]` Import Patterns. This is a third-party library, meaning you have to `pip install requests` for it to work. It handles the terrifying complexity of HTTP networks for us.
2. `def get_joke(topic=""):`
   - **Pattern:** `[L05]` Functions as Tools. We wrap the network request tightly inside a function so an Agent can use it cleanly.
3. `params = {"safe-mode": "true", ...}`
   - **Pattern:** `[L01]` Labels and Types (Dictionaries). The `requests` library turns this dictionary into the `?safe-mode=true&type=single` part of the URL URL automatically.
4. `try: ... except requests.exceptions.RequestException as e:`
   - **Pattern:** `[L09]` Error Reading / Error Handling. The network is unpredictable. Wi-Fi drops, servers crash. We wrap the call in a `try/except` block to gracefully catch crashes instead of breaking the entire script.
5. `response = requests.get(url, params=params)`
   - **Pattern:** `[L19]` API Request. The core pattern of this lesson.

## Pass 2: Quality Check (What's Hardcoded?)
* The URL `https://v2.jokeapi.dev/joke/Any` is hardcoded. If this API changes its URL or shuts down, our agent tool will instantly break.
* In a real production system, APIs often require an API key. We would need to pass `headers={"Authorization": f"Bearer {API_KEY}"}`, and the AI key should be securely loaded from a `.env` file!

## Pass 3: Extraction (What to Steal)
If you just want to make a safe API call to a specific URL and parse the JSON:
```python
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print("API failed:", response.status_code)
```
