# My Personal Template Library
## Organized by Lesson - Quick Reference for AI-Assisted Development

**Purpose:** Copy-paste templates when building AI systems. Never write from scratch.

**Philosophy:** These are NOT exercises. These are production patterns you'll use forever.

---

## 📁 Folder Structure

Templates live inside each lesson folder under `Phase1(A)/` (checked against the tree on 2026-10-28):

```
Phase1(A)/
├── L01_Labels_and_Types/             # Variables & Dictionaries
│   ├── CHEATSHEET_L01.py
│   ├── template_llm_metadata.py
│   ├── template_document_metadata.py
│   ├── template_agent_config.py
│   ├── template_structured_output.py
│   └── example_structured_output_demo.py
├── L02_Lists_and_Collections/        # Lists & Collections
│   ├── CHEATSHEET_L02.py
│   ├── template_list_operations.py
│   ├── template_conversation_history.py
│   └── VISUAL_conversation_flow.md
├── L03_Logic_Gates/                  # Logic Gates & Conditionals
│   ├── CHEATSHEET_L03.py
│   ├── template_confidence_threshold.py
│   ├── template_fallback_chains.py
│   ├── template_intent_routing.py
│   ├── template_safety_guards.py
│   └── template_source_validation.py
├── L04_Loops_and_Iteration/          # Loops & Iteration
│   ├── CHEATSHEET_L04.py
│   ├── template_count_sum.py
│   ├── template_filter_collection.py
│   └── template_find_first.py
├── L05_Functions_as_Tools/           # template_llm_caller.py, template_prompt_formatter.py, template_rag_pipeline.py
├── L06_Classes_as_Blueprints/        # template_conversation_agent.py, template_multi_tool_agent.py, template_rag_agent.py
└── L07_Reading_Real_AI_Code/         # annotated examples, no templates
```

Phase 1(B) lessons (L08–L21) keep their own templates in their folders, and `Templates/` holds the shared `template_rag_pipeline.py`.

---

## 🎯 Quick Access by Lesson

### **[Lesson 01: Variables & Dictionaries](Phase1(A)/L01_Labels_and_Types/)** ✅
**What you'll find:**
- ✅ One-page cheatsheet (CHEATSHEET_L01.py)
- ✅ LLM metadata tracking template
- ✅ Document/search result storage template
- ✅ Agent configuration template
- ✅ Structured output template (force LLM to return JSON)
- ✅ Structured output demo (try it now!)

**When to use:**
- Storing LLM call information
- RAG search results
- Configuration settings
- Any labeled data storage
- Making LLM return specific JSON format

**Start here:** [Phase1(A)/L01_Labels_and_Types/CHEATSHEET_L01.py](Phase1(A)/L01_Labels_and_Types/CHEATSHEET_L01.py)

---

### **[Lesson 02: Lists & Collections](Phase1(A)/L02_Lists_and_Collections/)** ✅
**What you'll find:**
- ✅ One-page cheatsheet (CHEATSHEET_L02.py)
- ✅ 10 common list patterns (list operations template)
- ✅ Conversation history template (chatbot context)
- ✅ Visual guide to how chatbots work

**When to use:**
- Managing multiple items (search results, messages)
- Building chatbot conversation history
- Filtering and sorting results
- Token tracking, error collection
- Source attribution

**Start here:** [Phase1(A)/L02_Lists_and_Collections/CHEATSHEET_L02.py](Phase1(A)/L02_Lists_and_Collections/CHEATSHEET_L02.py)

---

### **[Lesson 03: Logic Gates](Phase1(A)/L03_Logic_Gates/)** ✅
**What you'll find:**
- ✅ One-page cheatsheet (CHEATSHEET_L03.py)
- ✅ Confidence threshold, fallback chain, intent routing, safety guard and source validation templates

---

### **[Lesson 04: Loops & Iteration](Phase1(A)/L04_Loops_and_Iteration/)** ✅
**What you'll find:**
- ✅ One-page cheatsheet (CHEATSHEET_L04.py)
- ✅ Count/sum, filter-collection and find-first templates

---

## 🚀 How to Use These Templates

### **Method 1: The Copy-Paste Workflow**

1. **Open the template** that matches what you need
2. **Copy the entire code block**
3. **Ask Claude:** "Modify this template for [your use case]"
4. **Review the changes** using your bug detection skills
5. **Use it in your project**

**Example:**
```
You: "Modify template_llm_metadata.py to track OpenAI calls instead of Anthropic"
Claude: [generates modified code]
You: [review using checklist from cheatsheet]
```

---

### **Method 2: The Reference Lookup**

1. **Encounter a pattern** in AI-generated code
2. **Open CHEATSHEET_L01.py**
3. **Find the matching pattern**
4. **Verify** the AI code follows the pattern

**Example:**
- AI generates: `{"model": "gpt-4", "tokens" = 1500}`
- You check cheatsheet: "Wait, should be `:` not `=`"
- You catch the bug in 5 seconds

---

### **Method 3: The Template-First Approach**

1. **Before asking AI** to generate code
2. **Find the relevant template**
3. **Include it in your prompt:**
   "Generate code following this pattern: [paste template]"
4. **AI will match your style**

**Example:**
```
You: "Create a function to track LLM calls. Follow this pattern:
[paste template_llm_metadata.py]
But add fields for user_id and session_id"

Claude: [generates code matching your template]
```

---

## ✅ Your Workflow Checklist

**Before Writing Code:**
- [ ] Check if a template exists for this pattern
- [ ] Copy the template as starting point
- [ ] Modify only the values, keep the structure

**When AI Generates Code:**
- [ ] Compare to relevant template
- [ ] Check against cheatsheet red flags
- [ ] Verify syntax using visual patterns

**After Code is Written:**
- [ ] Run through checklist in CHEATSHEET_L01.py
- [ ] Spot check for common bugs
- [ ] Test with simple inputs

---

## 🎯 Real-World Example

**Scenario:** You're building a RAG system and need to store document metadata.

### **Old way (memorizing):**
- Try to remember dictionary syntax
- Wonder what fields you need
- Guess at naming conventions
- Make mistakes, debug for 20 minutes

### **New way (templates):**
1. Open `template_document_metadata.py`
2. Copy the pattern
3. Modify for your specific fields
4. Done in 2 minutes

---

## 📖 Template Quick Reference

### **When to use each template:**

**template_llm_metadata.py**
- ✅ Tracking LLM API calls
- ✅ Logging token usage
- ✅ Cost monitoring
- ✅ Performance metrics

**template_document_metadata.py**
- ✅ RAG search results
- ✅ Vector database queries
- ✅ Document retrieval
- ✅ Source attribution

**template_agent_config.py**
- ✅ Agent settings
- ✅ Tool configuration
- ✅ State tracking
- ✅ Budget monitoring

---

## 🔥 Pro Tips

### **Tip 1: Modify, Don't Memorize**
You don't need to remember the syntax. Just:
1. Copy template
2. Change the values
3. Move on

### **Tip 2: Keep Cheatsheet Open**
`CHEATSHEET_L01.py` should be open in a separate window while you code.

### **Tip 3: Build Your Library**
As you encounter new patterns, add them to this folder:
- `template_my_custom_pattern.py`
- Document what it does
- Reuse forever

### **Tip 4: Use Templates in Prompts**
Tell AI: "Follow this template: [paste code]"
- AI will match your style
- Consistent code structure
- Fewer bugs to catch

---

## 🎓 You've Completed Pass 3!

**What you now have:**
- ✅ 3 production-ready templates
- ✅ 1 one-page cheatsheet
- ✅ Personal reference library
- ✅ Workflow for using templates with AI

**What this means:**
- You'll never write dictionary syntax from scratch
- You'll catch bugs faster using the cheatsheet
- You'll direct AI more precisely with template references
- You're working like a real AI Architect!

---

## 🚀 Next Steps

**Immediate:**
1. Bookmark this folder
2. Print/pin `CHEATSHEET_L01.py` to your screen
3. Try one template with Claude

**Soon:**
1. Move to Lesson 02 (Lists)
2. Build more templates
3. Expand your reference library

**Goal:**
By Lesson 06, you'll have a complete template library covering all Python fundamentals for AI development.

---

**Remember:** The best AI Architects don't memorize. They reference. You're now set up to do exactly that.
