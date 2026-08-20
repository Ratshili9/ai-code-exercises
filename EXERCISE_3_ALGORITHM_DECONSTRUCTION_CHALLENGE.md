# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: Algorithm Deconstruction Challenge (`exercise-code-algorithms`)
**Author:** Talifhani  
**Language Selected:** Python (Python 3.11+)  
**Repository Path:** `use-cases/code-algorithms/python/TaskManager`  

---

## 1. Executive Summary & Challenge Objectives

In this exercise, we apply the prompt strategies from **Section 3: Deciphering Complex Functions and Algorithms** to analyze, deconstruct, and understand the non-trivial algorithmic modules in the Task Manager application.

We investigate three distinct algorithmic domains:
1. **Algorithm 1 — Free-Form Text Parsing (`task_parser.py`):** Step-by-step regex token extraction, relative temporal resolution, and input sanitization (Prompt 1 Workflow).
2. **Algorithm 2 — Multi-Factor Dynamic Priority Scoring (`task_priority.py`):** Deciphering weighted heuristics, status penalties, tag boosts, and ranking mechanics (Prompt 2 Workflow).
3. **Algorithm 3 — Two-Way Task List Synchronization & Conflict Resolution (`task_list_merge.py`):** Untangling complex control flow, Last-Write-Wins reconciliation, and domain state precedence invariants (Prompt 3 Workflow).
4. **Empirical Verification:** Verifying all 55 unit tests across the test suites.

---

## 2. Algorithm 1: Free-Form Text Parser (`task_parser.py`) — Prompt 1 Workflow

### 2.1 Code Under Investigation
The function `parse_task_from_text(text)` extracts structured task metadata from natural language string inputs (e.g., `"Finish client report !urgent #friday @work @urgent"`).

### 2.2 Algorithmic Breakdown & Execution Steps
The parser processes unstructured text in sequential phases:

```text
Raw Text Input: "Submit project proposal !3 #tomorrow @urgent @work"
       │
       ├─► Phase 1: Priority Extraction
       │   Regex: r'\s!([1-4]|urgent|high|medium|low)\b'
       │   Match: "!3" ──► TaskPriority.HIGH (3), stripped from text
       │
       ├─► Phase 2: Tag Extraction
       │   Regex: r'\s@(\w+)'
       │   Matches: ["urgent", "work"], stripped from text
       │
       ├─► Phase 3: Date Marker Extraction & Resolution
       │   Regex: r'\s#(\w+)'
       │   Match: "tomorrow" ──► today + timedelta(days=1)
       │   (Also resolves: 'today', 'next_week', 'monday'..'friday', 'YYYY-MM-DD')
       │
       ├─► Phase 4: Title Normalization
       │   Regex: r'\s+' ──► collapse multiple spaces and strip
       │   Title: "Submit project proposal"
       │
       ▼
Result: Task(title="Submit project proposal", priority=HIGH, due_date=2026-08-21, tags=['urgent', 'work'])
```

### 2.3 Concrete Example Trace
- **Input:** `"Deploy release !4 #monday @release"`
- **Trace:**
  1. *Priority:* Matches `!4` $\rightarrow$ sets `TaskPriority.URGENT`. Text becomes `"Deploy release #monday @release"`.
  2. *Tags:* Matches `@release` $\rightarrow$ `tags = ['release']`. Text becomes `"Deploy release #monday"`.
  3. *Date:* Matches `#monday`. `get_next_weekday(today, 0)` computes days ahead until next Monday.
  4. *Clean Title:* Normalized to `"Deploy release"`.
- **Output:** Fully populated `Task` object.

### 2.4 Complexity & Algorithmic Insights
- **Time Complexity:** $\mathcal{O}(N)$ where $N$ is text length (linear regex scanning and string substitutions).
- **Space Complexity:** $\mathcal{O}(N)$ for sub-string copies and token lists.
- **Edge Cases Identified:**
  - If multiple priority tokens exist (e.g., `!1 !4`), the regex `re.findall` captures all matches, but the code indexes `priority_matches[0]`, favoring the first token.
  - `#monday` calculation uses `days_ahead <= 0: days_ahead += 7`, ensuring that running on Monday schedules for *next* Monday rather than today.

---

## 3. Algorithm 2: Multi-Factor Priority Scoring (`task_priority.py`) — Prompt 2 Workflow

### 3.1 Code Under Investigation
`calculate_task_score(task)` computes a composite dynamic importance score used by `sort_tasks_by_importance()` to rank tasks.

### 3.2 Deciphering the Weighted Heuristic Formula
The algorithm combines multiple orthogonal dimensions into a single scalar value:

$$\text{Total Score} = \text{Base Priority} + \text{Due Date Proximity} + \text{Status Modifier} + \text{Tag Boost} + \text{Recency Boost}$$

```python
# Pseudocode of Scoring Heuristic:
score = base_priority_weight * 10       # LOW=10, MEDIUM=20, HIGH=40, URGENT=60

if task.has_due_date:
    if days_until_due < 0:   score += 35   # Overdue penalty boost
    elif days_until_due == 0: score += 20  # Due today
    elif days_until_due <= 2: score += 15  # Due within 48 hours
    elif days_until_due <= 7: score += 10  # Due this week

if task.status == DONE:     score -= 50   # Deprioritize completed items
elif task.status == REVIEW: score -= 15   # Deprioritize pending reviews

if has_any_tag(["blocker", "critical", "urgent"]):
    score += 8                            # Critical tag bonus

if days_since_last_update < 1:
    score += 5                            # Freshness bonus
```

### 3.3 Comparative Scenario Analysis

| Scenario | Priority | Due Date | Status | Tags | Score Breakdown | Total Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Overdue Blocker** | URGENT (60) | 2 days ago (+35) | IN_PROGRESS (0) | `["blocker"]` (+8) | $60 + 35 + 0 + 8 + 5$ | **108** |
| **B: High Priority Done** | HIGH (40) | Tomorrow (+15) | DONE (-50) | `[]` (0) | $40 + 15 - 50 + 5$ | **10** |
| **C: Medium Due Today** | MEDIUM (20) | Today (+20) | TODO (0) | `[]` (0) | $20 + 20 + 0 + 0 + 5$ | **45** |

### 3.4 Key Algorithmic Observations
- **Negative Balance Protection:** Even if a low-priority task is completed ($10 - 50 = -40$), the sorting `sort_tasks_by_importance()` handles negative numbers gracefully using standard integer comparison.
- **Stable Multi-Sort:** `sorted(task_scores, key=lambda x: x[0], reverse=True)` runs in $\mathcal{O}(M \log M)$ time using Timsort, where $M$ is the number of tasks.

---

## 4. Algorithm 3: Two-Way Task List Synchronization & Conflict Resolution (`task_list_merge.py`) — Prompt 3 Workflow

### 4.1 Code Under Investigation
`merge_task_lists(local_tasks, remote_tasks)` and `resolve_task_conflict(local_task, remote_task)` reconcile tasks between two asynchronous storage sources (local store and remote store).

### 4.2 Control Flow Decision Tree

```text
                     all_task_ids = Set(Local IDs) ∪ Set(Remote IDs)
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
     Only in Local              Only in Remote             Exists in Both
     (local_task only)          (remote_task only)         (Conflict Resolution)
             │                          │                          │
    to_create_remote           to_create_local             resolve_task_conflict()
                                                                   │
                                                ┌──────────────────┴──────────────────┐
                                                ▼                                     ▼
                                       Status Conflict?                       Field Resolution:
                                    (DONE vs non-DONE)                        (Timestamp comparison)
                                                │                                     │
                                   ┌────────────┴────────────┐            remote.updated_at > local.updated_at?
                                   ▼                         ▼                        │
                           One source is DONE:        Both non-DONE:         ┌────────┴────────┐
                           DONE status always         Latest updated_at      ▼                 ▼
                           wins unconditionally       wins status            Remote wins       Local wins
                                                                             (update local)    (update remote)
                                                                                      │
                                                                                      ▼
                                                                             Tag Resolution:
                                                                             Union: Set(local) ∪ Set(remote)
```

### 4.3 Key Domain Invariants in Conflict Resolution
1. **Completion Dominance Invariant:**
   ```python
   if remote_task.status == TaskStatus.DONE and local_task.status != TaskStatus.DONE:
       merged_task.status = TaskStatus.DONE
       merged_task.completed_at = remote_task.completed_at
       should_update_local = True
   ```
   *Rationale:* If a task was completed on either source, that completion must never be reverted by an older or concurrent in-progress state.
2. **Field-Level Last-Write-Wins (LWW):**
   - For `title`, `description`, `priority`, and `due_date`, the version with the newer `updated_at` timestamp takes precedence.
3. **Additive Tag Merging (CRDT Set Pattern):**
   - Tags are merged via union (`set(local.tags) | set(remote.tags)`), ensuring tags added on either device are preserved.
4. **Deep Copy Isolation:**
   - `merged_task = copy.deepcopy(local_task)` guarantees that mutations during conflict resolution do not corrupt original dictionary references.

### 4.4 Complexity Analysis
- **Time Complexity:** $\mathcal{O}(K)$ where $K = |Local| + |Remote|$ unique task IDs. Each conflict check is $\mathcal{O}(1)$ dictionary/field operations and $\mathcal{O}(T)$ for tag set union.
- **Space Complexity:** $\mathcal{O}(K)$ for the newly instantiated merged dictionary and mutation tracking maps (`to_create_remote`, `to_update_remote`, `to_create_local`, `to_update_local`).

---

## 5. Practical Verification & Test Suite Confirmation

### 5.1 Test Execution
We verified all three algorithms against ground truth by executing the entire test suite:

```bash
python -m unittest discover tests
```

- **Output:**
  ```text
  .......................................................
  ----------------------------------------------------------------------
  Ran 55 tests in 0.056s

  OK
  ```

### 5.2 Algorithmic Test Coverage Breakdown (55 Tests Total)
- **`test_task_parser.py` (8 tests):**
  - Text parsing with single/multiple tags (`@tag1 @tag2`)
  - Numeric priority (`!1` to `!4`) and named priority (`!urgent`)
  - Relative dates (`#today`, `#tomorrow`, `#next_week`, `#monday` through `#friday`, ISO dates)
  - Extra whitespace cleanup
- **`test_task_priority.py` (6 tests):**
  - Priority weight scoring (LOW vs URGENT)
  - Overdue score bonuses and near-due boosts
  - Status penalties for `DONE` and `REVIEW`
  - Tag bonuses (`blocker`, `critical`)
  - Sorting verification (`sort_tasks_by_importance`, `get_top_priority_tasks`)
- **`test_task_list_merge.py` (10 tests):**
  - Pure local creation and pure remote creation
  - Conflicting timestamps (remote newer vs local newer)
  - Completion dominance (remote `DONE` vs local `IN_PROGRESS`)
  - Tag union resolution
- **`test_task_manager.py` (31 tests):**
  - CRUD operations, persistence, and status filtering

---

## 6. Final Reflection on Algorithm Deconstruction

### 6.1 Explicit Curriculum Reflection Questions

#### Q1: How did AI change or deepen your understanding of these algorithms?
- **Response:** AI enabled me to look past raw syntactic lines and view the algorithms conceptually. For example, rather than viewing `task_list_merge.py` as a tangled cluster of `if/else` statements, AI helped me map it into three clean mathematical invariants: Last-Write-Wins (LWW) for metadata, Dominance hierarchy for completion status, and Set-Union for tags.

#### Q2: What remained difficult or counter-intuitive even after AI explanation?
- **Response:** Managing temporal edge cases in `task_parser.py` (specifically weekday math with `days_ahead <= 0: days_ahead += 7`). Understanding why running a parser on a Monday targeting `#monday` intentionally schedules for the *following* Monday (7 days ahead) rather than same-day required careful boundary tracing.

#### Q3: How would you explain this algorithm to another junior developer?
- **Response:** I would explain the two-way sync algorithm using a "Shared Notebook" analogy:
  - If a page only exists in your notebook, give a copy to your colleague.
  - If it only exists in theirs, take a copy.
  - If you both wrote on the same page, keep whichever title/description is newer, merge all topic tags together, and if either of you checked off "DONE", it stays DONE forever.

#### Q4: How did you test your understanding against AI?
- **Response:** I tested my comprehension by designing concrete edge-case scenarios (e.g., Scenario A, B, and C in Section 3.3 for priority scoring, and testing conflicting status vs newer timestamp in two-way merge) and comparing my calculated manual outputs against the AI's step-by-step trace and unit test assertions.

#### Q5: How could these algorithms be improved or optimized in the future?
- **Response:**
  1. *Parser:* Replace multiple regex passes with a single-pass token lexer to avoid repetitive string manipulation.
  2. *Sync:* Introduce cryptographic content hashing or version vectors (vector clocks) instead of relying strictly on wall-clock timestamps (`updated_at`), which are vulnerable to system clock skew.
  3. *Scoring:* Allow custom weighting configuration rather than hardcoding static integer constants.

---

## 7. Submission Summary

```text
================================================================================
        EXERCISE SUBMISSION: ALGORITHM DECONSTRUCTION CHALLENGE
================================================================================
Student: Talifhani
Repository Path: use-cases/code-algorithms/python/TaskManager

1. DECONSTRUCTED ALGORITHMS:
   - task_parser.py: Natural language token parser with weekday temporal offset math.
   - task_priority.py: Multi-factor composite heuristic ranking algorithm.
   - task_list_merge.py: Two-Way Synchronization with Last-Write-Wins and Completed-Wins rules.

2. VERIFIED COMPUTATIONAL COMPLEXITIES:
   - Text Parsing: O(N) linear text scanning.
   - Priority Scoring & Sort: O(M log M) Timsort over computed heuristics.
   - Conflict Merge: O(K) linear scan over combined task ID sets.

3. EMPIRICAL VALIDATION:
   - 55 unit tests passing across all 4 test suites.
================================================================================
```
