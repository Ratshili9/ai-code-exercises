# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: Learning a New Programming Language with AI (`exercise-new-language`)
**Author:** Talifhani  
**Language Track:** Python (Python 3.11+)  
**Repository Path:** `learning-with-ai/new-language/python`  
**Target Modules:** `text_processor.py`, `test_text_processor.py`  

---

## 1. Executive Summary & Module Objectives

In this exercise, we apply the **Four-Step Prompting Strategy** and advanced AI-assisted learning patterns to acquire structured mastery of a programming language without developing dependency on code generation.

The workflow followed four core phases:
1. **Part 1 — Learning Journey Plan:** Defining multi-phase progression milestones from fundamentals to production tooling.
2. **Part 2 — The 4-Step Prompting Pattern:**
   - Step 1: Conceptual & philosophical foundations.
   - Step 2: Step-by-step architectural breakdown.
   - Step 3: Guided hands-on implementation.
   - Step 4: Empirical verification and Gotcha elimination.
3. **Part 3 — Advanced Prompting Techniques:** Employing contextual analogies, Socratic tutoring, and the Feynman technique.
4. **Part 4 — Mini-Project Implementation & Validation:** Developing and testing an automated **Text Analysis & Token Frequency Processor** (`text_processor.py`).

---

## 2. Part 1: Structured Learning Journey Plan

```markdown
### Target: Enterprise Application & Tooling Mastery
- Phase 1: Core Fundamentals & Type System (Primitive types, memory model, scoping rules).
- Phase 2: Object-Oriented & Modular Design (Encapsulation, composition, interfaces).
- Phase 3: Collections & Standard Library Ecosystem (Iterators, streams, regex, I/O handling).
- Phase 4: Automated Testing & Tooling (Unittest / Pytest, dependency management, CI).
```

---

## 3. Part 2 & 3: The 4-Step Prompting Strategy Applied

### 3.1 Step 1: Conceptual Understanding
> *"Before diving into code: What are the core design philosophies and mental models required for this language? What are common misconceptions?"*

### 3.2 Step 2: Step-by-Step Breakdown
> *"Break down the implementation of token sanitization and frequency counting without writing full code yet. What data structures are most optimal for constant-time lookups?"*

### 3.3 Step 3: Guided Implementation
> *"Guide me through constructing the `TextProcessor` class, explaining the role of `Counter` from `collections` and regular expression compilation."*

### 3.4 Step 4: Verification & Socratic Feedback
> *"Here is my implementation. Critique it for gotchas, boundary conditions (such as empty or non-string inputs), and performance bottlenecks."*

---

## 4. Part 4: Mini-Project Implementation (`text_processor.py`)

```python
class TextProcessor:
    STOP_WORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "is", "it", "of", "as"}

    @classmethod
    def clean_and_tokenize(cls, text: str) -> List[str]:
        if not text or not isinstance(text, str):
            return []
        cleaned = re.sub(r"[^\w\s]", "", text.lower())
        return [token for token in cleaned.split() if token]

    @classmethod
    def analyze_frequencies(cls, tokens: List[str], top_n: int = 5) -> List[Tuple[str, int]]:
        filtered = [t for t in tokens if t not in cls.STOP_WORDS]
        return Counter(filtered).most_common(top_n)
```

### Automated Unit Test Validation (`test_text_processor.py`):
```text
Ran 4 tests in 0.000s
OK
```

---

## 5. Submission Summary

```text
================================================================================
          EXERCISE SUBMISSION: LEARNING A NEW PROGRAMMING LANGUAGE
================================================================================
Student: Talifhani
Language Track: Python (Python 3.11+)
Target Repository: learning-with-ai/new-language/python/

1. METHODOLOGY DEMONSTRATED:
   - 4-Step Prompting Pattern (Concept -> Breakdown -> Implementation -> Verification).
   - Applied Socratic tutoring and the Feynman technique to validate language idioms.
   - Built and tested an automated Text Processing Mini-Project.

2. VERIFICATION STATUS:
   - Automated unit test suite: 4/4 passing assertions (test_text_processor.py).
================================================================================
```
