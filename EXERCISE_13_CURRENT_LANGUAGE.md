# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: Applying AI to Deepen Programming Language Understanding (`exercise-current-language`)
**Author:** Talifhani  
**Language Selected:** Python (Python 3.11+)  
**Repository Path:** `learning-with-ai/current-language/python`  
**Target Modules:** `idiomatic_transformation.py`, `advanced_decorators.py`, `test_advanced_features.py`  

---

## 1. Executive Summary & Module Objectives

In this exercise, we practice using Generative AI prompt workflows to deepen our fluency in **Python**, moving beyond basic syntax to master language idioms, clean-code heuristics, and advanced metaprogramming features.

We executed three key learning activities:
1. **Activity 1 — Idiomatic Code Transformation:** Refactoring procedural loops into expressive comprehensions, pattern matching, and type annotations.
2. **Activity 2 — Code Quality Detective:** Developing an automated code-review checklist targeting Python-specific code smells and maintainability anti-patterns.
3. **Activity 3 — Advanced Language Features (Custom Parameterized Decorators):** Constructing production-grade decorators using `@functools.wraps` for retry backoff mechanisms and execution performance benchmarking.

---

## 2. Activity 1: Idiomatic Code Transformation

### 2.1 Side-by-Side Comparison

```python
# --- Procedural / Non-Idiomatic (Before) ---
def process_active_users_procedural(user_records):
    results = []
    total_score = 0
    count = 0
    for i in range(len(user_records)):
        user = user_records[i]
        if user.get("is_active") == True:
            if "score" in user and user["score"] is not None:
                score = user["score"]
                total_score = total_score + score
                count = count + 1
                formatted = {
                    "id": user["id"],
                    "username": user["username"].lower().strip(),
                    "score": score,
                    "tier": "High" if score >= 80 else ("Medium" if score >= 50 else "Low")
                }
                results.append(formatted)
    avg = total_score / count if count > 0 else 0.0
    return {"users": results, "average_score": avg}
```

```python
# --- Modern Idiomatic Python 3.11+ (After) ---
def process_active_users_idiomatic(user_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    def categorize_tier(score: float) -> str:
        match score:
            case s if s >= 80: return "High"
            case s if s >= 50: return "Medium"
            case _: return "Low"

    active_users = [
        {
            "id": u["id"],
            "username": u["username"].strip().lower(),
            "score": u["score"],
            "tier": categorize_tier(u["score"])
        }
        for u in user_records
        if u.get("is_active") and u.get("score") is not None
    ]

    avg_score = (
        sum(u["score"] for u in active_users) / len(active_users)
        if active_users else 0.0
    )
    return {"users": active_users, "average_score": round(avg_score, 2)}
```

### 2.2 Key Learnings:
1. **Comprehensions over Manual Accumulators:** List comprehensions with embedded filtering reduce boiler-plate loop counters and index variables.
2. **Structural Pattern Matching (`match/case`):** Python 3.10+ pattern matching provides cleaner branching semantics than nested ternary operators.
3. **Type Hinting & Static Safety:** Adding type annotations (`List[Dict[str, Any]]`) enables IDE autocompletion and static type checkers like `mypy`.

---

## 3. Activity 2: Code Quality Detective (Checklist)

| Check Category | Anti-Pattern / Code Smell | Pythonic Standard Practice |
| :--- | :--- | :--- |
| **Index Access** | `for i in range(len(items)):` | `for item in items:` or `for i, item in enumerate(items):` |
| **Boolean Checks** | `if flag == True:` | `if flag:` |
| **Resource Management**| Manual `f.close()` | Context managers (`with open(...) as f:`) |
| **Default Arguments** | Mutable defaults `def f(data=[]):` | Immutable sentinel `def f(data=None): data = data or []` |
| **String Formatting** | `total = total + str(x)` or `%` | f-strings `f"Total: {total}"` |

---

## 4. Activity 3: Advanced Language Features (Custom Decorators)

We implemented parameterized decorators with metadata preservation:

```python
import functools
import time
from typing import Callable, Any, TypeVar

F = TypeVar('F', bound=Callable[..., Any])

def retry(max_attempts: int = 3, delay: float = 0.05, backoff: float = 2.0):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts:
                        raise exc
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator
```

### Automated Unit Test Validation (`test_advanced_features.py`):
```text
Ran 5 tests in 0.087s
OK
```

---

## 5. Submission Summary

```text
================================================================================
  EXERCISE SUBMISSION: DEEPENING PROGRAMMING LANGUAGE UNDERSTANDING
================================================================================
Student: Talifhani
Language Track: Python (Python 3.11+)
Target Modules: learning-with-ai/current-language/python/

1. DELIVERABLES COMPLETED:
   - Idiomatic transformations (List comprehensions, match-case, type annotations).
   - Code quality review checklist for Python engineering standards.
   - Advanced metaprogramming: Parameterized retry backoff & timing decorators.

2. EMPIRICAL VALIDATION:
   - Automated unit test suite: 5/5 passing assertions (test_advanced_features.py).
================================================================================
```
