"""
CHEATSHEET L18: Persistence and Databases
Concepts: JSON encoding, File I/O (Input/Output)

STORAGE DECISION GUIDE — pick the right tool for the job:

  JSON file      → config, small state, single-user, human-readable  (< 10K records)
  SQLite         → structured data, queries, multi-table, local app   (< 1M records)
  PostgreSQL     → multi-user, concurrent writes, production backend  (any scale)
  Redis          → session cache, rate limits, ephemeral fast reads   (in-memory)
  Vector DB      → semantic search, embeddings, RAG retrieval         (Chroma, Pinecone)
  Object storage → binary files, large blobs, model artifacts         (S3, GCS)

  Rule of thumb: JSON until it breaks. SQLite until you need a server.
"""
import json
import os

# ==========================================
# PATTERN 1: Saving a Dictionary to JSON
# ==========================================
# The data we want to keep after the script ends
history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
]

# 'w' means Write mode (overwrites existing file)
with open("chat_log.json", "w") as f:
    # json.dump(data, file) -> converts Python list/dict to text and saves it
    json.dump(history, f, indent=4)  # indent=4 makes it readable for humans

print("Saved cleanly to chat_log.json")

# ==========================================
# PATTERN 2: Loading a Dictionary from JSON
# ==========================================
# 'r' means Read mode
with open("chat_log.json", "r") as f:
    # json.load(file) -> reads text and converts back to Python list/dict
    loaded_data = json.load(f)

print("Loaded from file:", loaded_data[0]["role"])


# ==========================================
# PATTERN 3: Safe Loading (Checking if file exists first)
# ==========================================
filename = "user_preferences.json"

if os.path.exists(filename):
    # The file is there, we can open it safely
    with open(filename, "r") as f:
        prefs = json.load(f)
        print("Loaded existing prefs.")
else:
    # File doesn't exist yet, make default prefs and save them
    prefs = {"theme": "dark", "language": "en"}
    with open(filename, "w") as f:
        json.dump(prefs, f)
        print("Created new default prefs.")
