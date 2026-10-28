"""
╔═══════════════════════════════════════════════════════════════════════════╗
║              MY PYTHON CHEAT SHEET - LESSON 1.5                           ║
║                    Lists & Collections Reference                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

Keep this file open while coding. Copy patterns as needed.
Last updated: 2026-02-27
"""

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: CREATING LISTS
# ═══════════════════════════════════════════════════════════════════════════

# Simple list
tools = ["search", "summarize", "translate"]

# List of numbers
scores = [0.95, 0.88, 0.92]

# Empty list (to build later)
messages = []

# List of dictionaries (MOST COMMON IN AI!)
results = [
    {"source": "Wikipedia", "score": 0.95},
    {"source": "ArXiv", "score": 0.88}
]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: ACCESSING ITEMS (Indexing)
# ═══════════════════════════════════════════════════════════════════════════

tools = ["search", "summarize", "translate"]

# First item (index 0)
first = tools[0]          # "search"

# Second item (index 1)
second = tools[1]         # "summarize"

# Last item (negative index)
last = tools[-1]          # "translate"

# Second-to-last item
second_last = tools[-2]   # "summarize"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: ADDING ITEMS
# ═══════════════════════════════════════════════════════════════════════════

conversation = []

# Add to end
conversation.append("User: Hello")
conversation.append("Agent: Hi there!")

# Add at specific position
conversation.insert(0, "System: Conversation started")

# Add multiple items
new_messages = ["User: How are you?", "Agent: I'm good!"]
conversation.extend(new_messages)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: REMOVING ITEMS
# ═══════════════════════════════════════════════════════════════════════════

sources = ["Wikipedia", "ArXiv", "Broken Link", "GitHub"]

# Remove by value
sources.remove("Broken Link")
# Now: ["Wikipedia", "ArXiv", "GitHub"]

# Remove by index and return it
removed = sources.pop(0)  # Removes "Wikipedia", returns it

# Remove last item
last = sources.pop()      # Removes and returns last item


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: LIST OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

scores = [0.95, 0.88, 0.92, 0.85]

# Count items
count = len(scores)              # 4

# Check if item exists
if 0.95 in scores:              # True
    print("Found it")

# Get max/min
highest = max(scores)            # 0.95
lowest = min(scores)             # 0.85

# Sum of all items
total = sum(scores)              # 3.60

# Sort (modifies original)
scores.sort()                    # [0.85, 0.88, 0.92, 0.95]
scores.sort(reverse=True)        # [0.95, 0.92, 0.88, 0.85]

# Sort (creates new list)
sorted_scores = sorted(scores)   # Original unchanged


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: LIST OF DICTIONARIES (THE AI PATTERN!)
# ═══════════════════════════════════════════════════════════════════════════

# This is THE most common pattern in AI systems!
search_results = [
    {"source": "Wikipedia", "score": 0.95, "verified": True},
    {"source": "Blog", "score": 0.72, "verified": False},
    {"source": "ArXiv", "score": 0.88, "verified": True}
]

# Access first result
first_result = search_results[0]
# Returns: {"source": "Wikipedia", "score": 0.95, ...}

# Access first result's score (two-level access!)
first_score = search_results[0]["score"]
# Returns: 0.95

# Safe access
score = search_results[0].get("score", 0.0)

# Count results
num_results = len(search_results)  # 3


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: COMMON PATTERNS IN AI
# ═══════════════════════════════════════════════════════════════════════════

# Pattern 1: Conversation History
conversation = []
conversation.append({"role": "user", "content": "Hello"})
conversation.append({"role": "assistant", "content": "Hi there!"})

# Pattern 2: Source Attribution
sources_used = []
sources_used.append("Wikipedia")
sources_used.append("ArXiv")

# Pattern 3: Error Collection
errors = []
if something_wrong:
    errors.append({"step": "search", "error": "Failed"})

# Pattern 4: Token Tracking
tokens_used = []
tokens_used.append(1523)
tokens_used.append(892)
total = sum(tokens_used)

# Pattern 5: Building Filtered Results
high_quality = []
for result in all_results:  # You'll learn loops in Lesson 04
    if result["score"] >= 0.85:
        high_quality.append(result)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8: RED FLAGS TO SPOT (Bug Detector)
# ═══════════════════════════════════════════════════════════════════════════

# ❌ Index out of range
tools = ["search", "summarize"]
# wrong = tools[5]              # IndexError: list index out of range
right = tools[0]                # Access valid index

# ❌ Modifying list while looping (DANGEROUS!)
# for item in my_list:
#     my_list.remove(item)      # ⚠️ Causes skipping/crashes!
# Use list comprehension instead (learn in Lesson 04)

# ❌ Forgetting lists start at 0
tools = ["search", "summarize", "translate"]
# first = tools[1]              # ❌ This is the SECOND item!
first = tools[0]                # ✅ This is the first item

# ❌ Accessing dict in list without checking
results = [{"score": 0.95}]
# wrong = results[0]["confidence"]  # KeyError if key doesn't exist
right = results[0].get("confidence", 0.0)  # Safe access

# ❌ Not checking if list is empty
results = []
# first = results[0]            # IndexError: list index out of range
if len(results) > 0:            # Check first
    first = results[0]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 9: VISUAL SHAPES TO RECOGNIZE
# ═══════════════════════════════════════════════════════════════════════════

"""
SHAPE             EXAMPLE                          MEANING
────────────────────────────────────────────────────────────────────────
Simple list       ["a", "b", "c"]                  Ordered items
Empty list        []                               To build later
List of numbers   [0.95, 0.88, 0.92]              Scores, metrics
List of dicts     [{"key": "val"}, ...]           Search results
Nested list       [[a, b], [c, d]]                Multi-level data
First item        list[0]                          Index 0
Last item         list[-1]                         Negative index
Two-level access  list[0]["key"]                   List then dict
Count items       len(list)                        Number of items
Add to end        list.append(item)                Grow the list
Check exists      if item in list:                 Membership test
"""


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 10: MY CODE REVIEW CHECKLIST
# ═══════════════════════════════════════════════════════════════════════════

"""
When reviewing list code, check:

SYNTAX:
[ ] Square brackets [] used correctly
[ ] Commas separate items
[ ] Indices are valid (0 to len-1)
[ ] Negative indices used correctly (-1 = last)

SAFETY:
[ ] Check if list is empty before accessing
[ ] Use .get() for dict keys in list
[ ] Don't modify list while iterating over it
[ ] Handle index out of range errors

PATTERNS:
[ ] Using .append() to grow lists
[ ] Using len() to count items
[ ] List of dicts for structured data
[ ] Empty list initialized before building

COMMON USE CASES:
[ ] Conversation history: list of message dicts
[ ] Search results: list of document dicts
[ ] Error tracking: list of error dicts
[ ] Source attribution: list of source names
[ ] Token tracking: list of numbers
"""


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 11: QUICK REFERENCE - MOST USED OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

# Create
my_list = []                     # Empty
my_list = ["a", "b", "c"]       # With items

# Access
first = my_list[0]              # First item
last = my_list[-1]              # Last item
second = my_list[1]             # Second item

# Modify
my_list.append(item)            # Add to end
my_list.remove(item)            # Remove by value
my_list.pop()                   # Remove last
my_list.insert(0, item)         # Add at position

# Check
count = len(my_list)            # How many items
if item in my_list:             # Does it exist?
if len(my_list) > 0:           # Is it not empty?

# Operations
total = sum(numbers)            # Sum of numbers
highest = max(numbers)          # Highest value
lowest = min(numbers)           # Lowest value
my_list.sort()                  # Sort in place


# ═══════════════════════════════════════════════════════════════════════════
# END OF CHEAT SHEET
# ═══════════════════════════════════════════════════════════════════════════
# Keep this file open as reference. Copy patterns as needed. Don't memorize!
