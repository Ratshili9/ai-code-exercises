# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: AI Solution Verification Challenge (`exercise-debug-limitations`)
**Author:** Talifhani  
**Language Selected:** Python (Python 3.11+)  
**Repository Path:** `use-cases/debug-limitations/python`  
**Target Code Module:** `merge_sort.py`  

---

## 1. Executive Summary & Challenge Objectives

In this exercise, we practice applying a critical verification mindset when using AI tools for debugging. Rather than accepting AI suggestions blindly, we evaluate edge cases, detect subtle logic errors (such as infinite loops), and verify solutions through rigorous automated testing.

We investigated the **Merge Sort Implementation Defect** and applied the verification prompts from **Section 3: Limitations and Verification**:
1. **Prompt 1 (Collaborative Solution Verification):** Designing comprehensive test cases beyond the happy path (empty arrays, single elements, duplicates, reverse sorted, negative numbers).
2. **Prompt 2 (Learning Through Alternative Approaches):** Comparing iterative merge sort vs. recursive slice-based merge sort.
3. **Prompt 3 (Developing a Critical Eye):** Catching variable pointer mis-increments (such as incrementing the wrong pointer `j` inside a `while (i < len(left))` loop).

---

## 2. Section 1: Defect Diagnosis & Root Cause Analysis

### 2.1 Python Implementation (`use-cases/debug-limitations/python/merge_sort.py`)
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Draining remaining left elements
    while i < len(left):
        result.append(left[i])
        i += 1  # Crucial: Must increment i, not j

    # Draining remaining right elements
    while j < len(right):
        result.append(right[j])
        j += 1

    return result
```

### 2.2 Root Cause & Failure Mechanism
When the `left` sub-array has remaining elements after the main zip-loop finishes (e.g. `left = [5, 8]`, `right = [1, 2]`), the left-drain loop begins. 
If an AI or developer mistakenly increments `j` instead of `i` inside `while i < len(left):`, the value of `i` never advances, causing an infinite loop where memory expands indefinitely and the program crashes.

---

## 3. Section 2: Automated Verification Suite (`test_merge_sort.py`)

We created and executed a full `unittest` suite validating the algorithm across all boundary conditions:

```python
import unittest
from merge_sort import merge_sort

class TestMergeSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        self.assertEqual(merge_sort([42]), [42])

    def test_already_sorted(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        # Triggers left-dominant drain loop
        self.assertEqual(merge_sort([9, 7, 5, 3, 1]), [1, 3, 5, 7, 9])

    def test_duplicates(self):
        self.assertEqual(merge_sort([5, 1, 5, 3, 1]), [1, 1, 3, 5, 5])

    def test_negative_numbers(self):
        self.assertEqual(merge_sort([-3, -10, 5, 0, -1]), [-10, -3, -1, 0, 5])

if __name__ == "__main__":
    unittest.main()
```

### Test Results:
```text
Ran 6 tests in 0.000s
OK
```

---

## 4. Section 3: Reflection on AI Limitations & Verification Mindset

1. **AI Hallucinations & Syntax Blindspots:** AI models can generate plausible-looking loops with subtle index/pointer mix-ups (like `j++` in an `i` loop). Human inspection of loop invariants and boundaries is indispensable.
2. **Never Skip Edge Cases:** Testing solely with balanced inputs (e.g., alternating numbers) can accidentally mask single-sided drain loop bugs.
3. **The Principle to Verify:** Always test AI-suggested code empirically with automated unit tests before deploying to production.

---

## 5. Submission Summary

```text
================================================================================
        EXERCISE SUBMISSION: AI SOLUTION VERIFICATION CHALLENGE
================================================================================
Student: Talifhani
Language: Python (and JavaScript starter)
Module Target: use-cases/debug-limitations/python/merge_sort.py

1. DEFECT RESOLVED:
   - Verified recursive merge sort invariants across 6 critical edge cases.
   - Guarded against infinite loops caused by pointer mismatches.

2. VERIFICATION PRINCIPLE APPLIED:
   - Evaluated solution boundaries, memory stability, and reverse-sorted scenarios.
   - Built full automated test suite passing 100% of test assertions.
================================================================================
```
