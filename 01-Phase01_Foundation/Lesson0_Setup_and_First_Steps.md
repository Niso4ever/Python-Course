# Lesson 0: Python Setup & First Steps
## The Foundation Before the Foundation

Welcome, future AI Architect. Before we can build intelligent systems, we need to set up our construction site and learn the most fundamental rule of programming: **The computer reads your instructions one line at a time, from top to bottom.**

---

## Part 1: Setting Up Your Workshop

### What is Python?
Python is a **programming language** — a way to give instructions to a computer. Think of it as the language an architect uses to communicate with construction workers. When you write Python code, you're writing a recipe that the computer follows exactly.

### Installing Python

**Check if Python is Already Installed:**
Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:

```bash
python3 --version
```

If you see something like `Python 3.11.5`, you're ready! If not, follow these steps:

**Installation Steps:**
1. **Windows:** Download from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH" during installation
2. **Mac:** Python 3 usually comes pre-installed. If not, use `brew install python3`
3. **Linux:** Usually pre-installed. If not: `sudo apt install python3`

---

## Part 2: Your First Python Command

### The `print()` Function
The most fundamental tool in Python is `print()`. It displays messages on your screen — like an architect shouting instructions to the construction site.

**Create Your First Python File:**
1. Create a new file called `hello.py` in your AIarch folder
2. Open it in VS Code (or any text editor)
3. Type this exact line:

```python
print("Hello, Architect")
```

4. Save the file
5. Open your terminal in the same folder and run:

```bash
python3 hello.py
```

**What You Should See:**
```
Hello, Architect
```

🎉 **Congratulations!** You just gave your computer an instruction, and it followed it.

---

## Part 3: The Top-to-Bottom Rule

### How Python Reads Your Code
Python is not smart. It reads your code **one line at a time, from top to bottom**, and does exactly what you tell it.

**Example: The Order Matters**

```python
print("Step 1: Initializing system")
print("Step 2: Loading AI model")
print("Step 3: Ready to build")
```

**Output:**
```
Step 1: Initializing system
Step 2: Loading AI model
Step 3: Ready to build
```

Python reads line 1, executes it, then moves to line 2, executes it, and so on. **If you swap the lines, the output changes.**

---

## Part 4: Comments (Your Blueprint Notes)

### The `#` Symbol
When architects draw blueprints, they add notes like "Load-bearing wall" or "Reinforced steel here." In Python, we use the `#` symbol to write notes that Python **ignores**.

```python
# This is a note to myself — Python skips this line
print("This line runs")  # You can also add notes at the end of a line
```

**Why Use Comments?**
- To explain **why** you wrote something
- To leave notes for your future self
- To temporarily disable a line of code

```python
# Testing the greeting system
print("Welcome to the AI system")
# print("Debug mode active")  # This line is disabled
```

---

## Part 5: Understanding Errors (Your First Construction Failure)

### What Happens When You Make a Mistake?
Python will tell you. Let's deliberately break something to learn how to read error messages.

**Broken Code:**
```python
print("Hello Architect)
```

**Error Message:**
```
SyntaxError: unterminated string literal (detected at line 1)
```

**What This Means:**
- `SyntaxError`: You broke a grammar rule
- `unterminated string literal`: You started a quote `"` but never closed it
- `line 1`: The problem is on line 1

**Fixed Code:**
```python
print("Hello Architect")  # Both quotes match now
```

### Common Beginner Errors
| Error | Cause | Fix |
|:------|:------|:----|
| `SyntaxError: unterminated string literal` | Missing closing quote | Add `"` or `'` |
| `NameError: name 'Print' is not defined` | Wrong capitalization | Use `print` not `Print` |
| `IndentationError: unexpected indent` | Wrong whitespace | Remove extra spaces at the start |

---

## Part 6: The Terminal (Your Command Center)

### Running Python Code
You have two ways to run Python:

**Method 1: Running a File**
```bash
python3 my_code.py
```

**Method 2: Interactive Mode (REPL)**
Type `python3` in the terminal and press Enter. Now you can type Python commands directly:
```python
>>> print("Testing")
Testing
>>> 5 + 3
8
>>> exit()  # To leave interactive mode
```

**In this course you'll use `.py` files only — no Jupyter Notebooks (`.ipynb`).**

---

## Part 7: Intermediate Reinforcement

**Question 1:** What will this code print?
```python
print("AI")
print("Architect")
```

**Question 2:** Why doesn't this line do anything?
```python
# print("Secret message")
```

**Question 3:** What's wrong with this code?
```python
Print("Hello")
```

---

## Part 8: Interactive Training Ground

Now, prove you understand the basics. Create a file called `setup_practice.py`, write the missions below into it, and run it with `python setup_practice.py`.

**Mission:**
1. Print your name
2. Print 3 lines that simulate an AI agent starting up
3. Fix broken code with missing quotes
4. Add comments explaining what each line does

---

## Summary: What You've Learned

| Concept | Purpose |
|:--------|:--------|
| `print()` | Display messages on screen |
| `#` | Write comments that Python ignores |
| Top-to-Bottom | Python reads code line by line in order |
| Error Messages | Python tells you what went wrong and where |
| `.py` files | Where you write your Python instructions |

**Next Step:** Once you complete the practice file, you're ready for **[Lesson 01: Labels, Containers, and Types](Phase1(A)/L01_Labels_and_Types/L01_Labels_and_Types.md)**, where you'll learn to store and label data.

---

> **Note to Architect:** You're not expected to memorize everything. Programming is about **understanding the pattern**, then looking up the syntax when you need it. Keep this lesson open as a reference.
