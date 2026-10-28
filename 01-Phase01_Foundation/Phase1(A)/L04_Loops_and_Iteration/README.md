# Lesson 04 Templates: Loops & Iteration

These templates show common loop patterns for processing collections in AI systems.

## What's Inside

### Learning Materials
1. **PASS1_RECOGNITION.md** - Learn to recognize loops (START HERE!)
2. **PASS_C_VISUAL.md** - See loops as flowcharts and assembly lines
3. **PASS3_TEMPLATES.md** - Overview of all templates

### Templates
4. **CHEATSHEET_L04.py** - Quick reference (KEEP OPEN!)
5. **template_filter_collection.py** - Filter by criteria
6. **template_count_sum.py** - Count/sum values
7. **template_find_first.py** - Find first match

## How to Use These

**Your workflow:**
1. Identify your processing need
2. Find the matching template
3. Copy and modify
4. Use in your AI system

## Common Patterns

### Filter Collection
Use when: Keep only items matching criteria
```python
filtered = []
for item in items:
    if item["score"] > 0.80:
        filtered.append(item)
```

### Count/Sum
Use when: Calculate totals
```python
total = 0
for item in items:
    total += item["value"]
```

### Find First
Use when: Need first match, then stop
```python
for item in items:
    if matches(item):
        result = item
        break
```

### Extract Fields
Use when: Pull one field from all items
```python
names = []
for item in items:
    names.append(item["name"])
```

---

## Learning Path

### Step 1: Recognition (30 min)
Read [PASS1_RECOGNITION.md](PASS1_RECOGNITION.md)
- See 8 annotated examples
- Practice identifying patterns
- Do recognition exercises

### Step 2: Visual (15 min)
Study [PASS_C_VISUAL.md](PASS_C_VISUAL.md)
- View flowcharts and assembly lines
- Understand loop flow visually
- Practice mental visualization

### Step 3: Templates (15 min)
Browse [PASS3_TEMPLATES.md](PASS3_TEMPLATES.md)
- See all 12 templates
- Pick one that matches your need
- Copy and modify

### Step 4: Reference
Keep [CHEATSHEET_L04.py](CHEATSHEET_L04.py) open while coding!

---

**Remember:** You're not memorizing loop syntax. You're recognizing patterns like "filter RAG results" or "count tokens." The templates handle the rest.
