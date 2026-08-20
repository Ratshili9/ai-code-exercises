# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: AI Solution Verification Challenge (`exercise-debug-limitations`)
**Author:** Talifhani  
**Language Selected:** JavaScript / Python  
**Repository Path:** `use-cases/debug-limitations/javascript`  
**Target Code Module:** `merge_sort.js`  

---

## 1. Executive Summary & Challenge Objectives

In this exercise, we practice applying a critical verification mindset when using AI tools for debugging. Rather than accepting AI suggestions blindly, we evaluate edge cases, detect subtle logic errors (such as infinite loops), and verify solutions through rigorous testing.

We investigated the **Merge Sort Implementation Defect** (`merge_sort.js`) and applied the verification prompts from **Section 3: Limitations and Verification**:
1. **Prompt 1 (Collaborative Solution Verification):** Designing comprehensive test cases beyond the happy path (empty arrays, single elements, duplicates, reverse sorted).
2. **Prompt 2 (Learning Through Alternative Approaches):** Comparing in-place iterative merge sort vs. recursive slice-based merge sort.
3. **Prompt 3 (Developing a Critical Eye):** Catching variable pointer mis-increments (`j++` inside `while (i < left.length)`).

---

## 2. Section 1: Defect Diagnosis & Root Cause Analysis

### 2.1 Code Under Investigation (`merge_sort.js`)
```javascript
function merge(left, right) {
    let result = [];
    let i = 0;
    let j = 0;

    while (i < left.length && j < right.length) {
        if (left[i] < right[j]) {
            result.push(left[i]);
            i++;
        } else {
            result.push(right[j]);
            j++;
        }
    }

    // CRITICAL DEFECT: Incrementing j instead of i
    while (i < left.length) {
        result.push(left[i]);
        j++; // Causes infinite loop because `i` never advances!
    }

    while (j < right.length) {
        result.push(right[j]);
        j++;
    }

    return result;
}
```

### 2.2 Root Cause & Failure Mechanism
When the `left` sub-array has remaining elements after the main zip-loop finishes (e.g. `left = [5, 8]`, `right = [1, 2]`), the loop `while (i < left.length)` begins. 
Because line 30 incremented `j++` instead of `i++`, the value of `i` remained permanently `0`, causing the loop condition `0 < 2` to evaluate to `true` indefinitely. The process hung, consumed infinite memory, and timed out.

### 2.3 Verified Code Fix

```diff
--- merge_sort.js (Buggy)
+++ merge_sort.js (Fixed)
@@ -28,3 +28,3 @@
     while (i < left.length) {
         result.push(left[i]);
-        j++; // Bug: incrementing j instead of i
+        i++;
     }
```

---

## 3. Section 2: Verification Plan & Edge Cases

| Test Scenario | Input Array | Expected Output | Verification Purpose |
| :--- | :--- | :--- | :--- |
| **Empty Array** | `[]` | `[]` | Verifies base case $N=0$ |
| **Single Element** | `[42]` | `[42]` | Verifies base case $N=1$ |
| **Sorted Array** | `[1, 2, 3, 4]` | `[1, 2, 3, 4]` | Verifies right-dominant drain |
| **Reverse Sorted** | `[9, 7, 5, 3]` | `[3, 5, 7, 9]` | **Verifies left-dominant drain (triggers the fixed loop)** |
| **Duplicates** | `[5, 1, 5, 3, 1]` | `[1, 1, 3, 5, 5]` | Verifies stability with identical values |

---

## 4. Section 3: Reflection on AI Limitations & Verification Mindset

1. **AI Hallucinations & Syntax Blindspots:** AI models can sometimes generate plausible-looking loops with subtle index/pointer mix-ups (like `j++` in an `i` loop). Human inspection of variable invariants is indispensable.
2. **Never Skip Edge Cases:** Testing solely with balanced inputs (e.g., alternating numbers) can accidentally mask single-sided drain loop bugs.
3. **The Principle to Verify:** Always test AI-suggested code empirically with automated test suites before deploying to production.

---

## 5. Submission Summary

```text
================================================================================
        EXERCISE SUBMISSION: AI SOLUTION VERIFICATION CHALLENGE
================================================================================
Student: Talifhani
Module Target: use-cases/debug-limitations/javascript/merge_sort.js

1. DEFECT RESOLVED:
   - Fixed infinite loop caused by pointer mismatch (j++ -> i++ in left-drain loop).
   - Validated recursive merge sort invariants across 5 critical edge cases.

2. VERIFICATION PRINCIPLE APPLIED:
   - Evaluated solution boundaries, memory stability, and reverse-sorted scenarios.
================================================================================
```
