# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development

**Student / Author:** Talifhani  
**Track & Environment:** Python 3.11+ (Strictly Python)  
**Repository Status:** 100% Complete, Validated & Passing (135+ automated unit tests)

---

## 📚 Master Index of Completed Exercises & Deliverables

### Part 1: Using AI for Everyday Work
| # | Module | Exercise Title | Code Module / Path | Deliverable Report | Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| **1** | Comprehending Codebases | Knowing Where to Start | `use-cases/code-algorithms/python/TaskManager` | [`EXERCISE_1_KNOWING_WHERE_TO_START.md`](EXERCISE_1_KNOWING_WHERE_TO_START.md) | ✅ Complete |
| **2** | Comprehending Codebases | Codebase Exploration Challenge | `use-cases/code-algorithms/python/TaskManager` | [`EXERCISE_2_CODEBASE_EXPLORATION_CHALLENGE.md`](EXERCISE_2_CODEBASE_EXPLORATION_CHALLENGE.md) | ✅ Complete |
| **3** | Comprehending Codebases | Algorithm Deconstruction Challenge | `use-cases/code-algorithms/python/TaskManager` | [`EXERCISE_3_ALGORITHM_DECONSTRUCTION_CHALLENGE.md`](EXERCISE_3_ALGORITHM_DECONSTRUCTION_CHALLENGE.md) | ✅ Complete |
| **4** | Documentation | Code Documentation (Docstrings) | `use-cases/code-algorithms/python/TaskManager/task_list_merge.py` | [`EXERCISE_4_CODE_DOCUMENTATION.md`](EXERCISE_4_CODE_DOCUMENTATION.md) | ✅ Complete |
| **5** | Documentation | API Documentation | `POST /api/users/register` (Flask / OpenAPI) | [`EXERCISE_5_API_DOCUMENTATION.md`](EXERCISE_5_API_DOCUMENTATION.md) | ✅ Complete |
| **6** | Documentation | README & User Guide Documentation | `use-cases/code-algorithms/python/TaskManager` | [`EXERCISE_6_README_AND_USER_GUIDE.md`](EXERCISE_6_README_AND_USER_GUIDE.md) | ✅ Complete |
| **7** | Debugging Errors | Error Diagnosis Challenge | `use-cases/debug-errors-001/python/stock_manager.py` | [`EXERCISE_7_ERROR_DIAGNOSIS_CHALLENGE.md`](EXERCISE_7_ERROR_DIAGNOSIS_CHALLENGE.md) | ✅ Complete |
| **8** | Debugging Errors | Performance Optimization Challenge | `use-cases/debug-performance/python/inventory_analysis.py` | [`EXERCISE_8_PERFORMANCE_OPTIMIZATION_CHALLENGE.md`](EXERCISE_8_PERFORMANCE_OPTIMIZATION_CHALLENGE.md) | ✅ Complete |
| **9** | Debugging Errors | AI Solution Verification Challenge | `use-cases/debug-limitations/python/merge_sort.py` | [`EXERCISE_9_AI_SOLUTION_VERIFICATION_CHALLENGE.md`](EXERCISE_9_AI_SOLUTION_VERIFICATION_CHALLENGE.md) | ✅ Complete |
| **10** | Testing with AI | Using AI to Help with Testing | `use-cases/testing-001/python/TaskManager/tests` | [`EXERCISE_10_TESTING_WITH_AI.md`](EXERCISE_10_TESTING_WITH_AI.md) | ✅ Complete |
| **11** | Code Refactoring | Function Decomposition Challenge | `use-cases/refactor-functions/python/sales_report.py` | [`EXERCISE_11_FUNCTION_DECOMPOSITION.md`](EXERCISE_11_FUNCTION_DECOMPOSITION.md) | ✅ Complete |
| **12** | Code Refactoring | Design Pattern Implementation | `use-cases/refactor-patterns/python/database_connection.py` | [`EXERCISE_12_DESIGN_PATTERN_REFACTORING.md`](EXERCISE_12_DESIGN_PATTERN_REFACTORING.md) | ✅ Complete |

### Part 2: Learning with AI
| # | Module | Exercise Title | Code Module / Path | Deliverable Report | Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| **13** | Deepening Language Knowledge | Applying AI to Deepen Understanding | `learning-with-ai/current-language/python/` | [`EXERCISE_13_CURRENT_LANGUAGE.md`](EXERCISE_13_CURRENT_LANGUAGE.md) | ✅ Complete |
| **14** | Learning a New Language | 4-Step Prompting & Text Processor | `learning-with-ai/new-language/python/` | [`EXERCISE_14_LEARNING_NEW_LANGUAGE.md`](EXERCISE_14_LEARNING_NEW_LANGUAGE.md) | ✅ Complete |
| **15** | Frameworks & APIs | Getting Started with FastAPI CRUD API | `learning-with-ai/frameworks-fastapi/python/` | [`EXERCISE_15_LEARNING_FRAMEWORKS_FASTAPI.md`](EXERCISE_15_LEARNING_FRAMEWORKS_FASTAPI.md) | ✅ Complete |

---

## 🌟 The 5 Core Principles of AI-Assisted Engineering

1. **Communicate Clearly (SCSD Approach):** Be **Specific**, provide **Context**, use **Structured** formatting, and remain **Descriptive**.
2. **Verify!:** Continuously test AI assumptions with automated unit test suites and official documentation.
3. **Learn Through Guided Practice:** Utilize Socratic prompting and hints rather than blind code generation.
4. **Know Your Words:** Master software engineering terminology (e.g., refactoring, GoF patterns, invariants, Big-O complexity) to prompt effectively.
5. **Drive Your Own Learning:** Build learning journey roadmaps and take full ownership of code quality and architectural decisions.

---

## ⚙️ How to Run the Automated Test Suite

```bash
# Run all unit test suites across the repository:
python -m unittest discover use-cases/code-algorithms/python/TaskManager/tests
python -m unittest discover use-cases/debug-errors-001/python/tests
python -m unittest discover use-cases/debug-limitations/python
python -m unittest discover use-cases/refactor-functions/python
python -m unittest discover use-cases/refactor-patterns/python
python -m unittest discover use-cases/testing-001/python/TaskManager/tests
python -m unittest discover learning-with-ai/current-language/python
python -m unittest discover learning-with-ai/new-language/python
python -m unittest discover learning-with-ai/frameworks-fastapi/python
```
