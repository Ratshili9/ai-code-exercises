# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: Learning a New Framework, Library or API (FastAPI) (`exercise-sdk-fastapi` / `exercise-sdk-api`)
**Author:** Talifhani  
**Language Track:** Python (FastAPI, Pydantic, Uvicorn)  
**Repository Path:** `learning-with-ai/frameworks-fastapi/python`  
**Target Modules:** `app/models.py`, `app/main.py`, `test_fastapi_app.py`  

---

## 1. Executive Summary & Challenge Objectives

In this exercise, we practice using Generative AI prompt workflows to rapidly master a modern web framework (**FastAPI**), navigating from fundamental concepts through contextual comparison to building and testing a production-ready RESTful application.

The exercise covers four core areas:
1. **FastAPI Architecture & Design Philosophy:** Pydantic schema validation, OpenAPI auto-generation, and async-first routing.
2. **Contextual Translation Table:** Mapping familiar concepts from Flask/Django (Blueprints, Request Form Validation, Middleware) to FastAPI equivalents (`APIRouter`, `Depends`, Pydantic models).
3. **Documentation Navigation Strategy:** Using targeted queries to extract dependency injection and exception handling patterns directly from official docs.
4. **CRUD REST API Implementation & Testing:** Constructing a complete To-Do management system with pagination, status filtering, and dependency-injected timestamps.

---

## 2. Framework Comparison & Translation Table

| Concept Area | Flask / Django Equivalent | FastAPI Idiomatic Implementation |
| :--- | :--- | :--- |
| **Route Organization** | Flask `Blueprint` / Django `urls.py` | `fastapi.APIRouter(prefix="/items", tags=["items"])` |
| **Data Validation** | Django `forms.Form` / manual dict parsing | `pydantic.BaseModel` schemas with type hints & field bounds |
| **Middleware & Cross-Cutting** | Flask `@before_request` / Django Middleware | `fastapi.Depends(...)` dependency injection & custom middleware |
| **API Documentation** | Manual Swagger/Postman setups | Automatic interactive docs generated at `/docs` (Swagger UI) & `/redoc` |
| **Asynchronous I/O** | WSGI sync (Flask) / Async views (Django 4+) | Native ASGI async/await route handlers (`async def endpoint(...)`) |

---

## 3. Implementation Overview (`learning-with-ai/frameworks-fastapi/python`)

### 3.1 Pydantic Validation Models (`app/models.py`)
```python
from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    created_at: str
```

### 3.2 Endpoint Handlers & Dependency Injection (`app/main.py`)
```python
from fastapi import FastAPI, HTTPException, Query, Path, status, Depends
from .models import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(title="FastAPI Todo API")

def get_current_timestamp() -> str:
    return datetime.utcnow().isoformat()

@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, timestamp: str = Depends(get_current_timestamp)):
    # Dependency-injected timestamp with automatic Pydantic request validation
    ...
```

---

## 4. Automated Test Suite Validation (`test_fastapi_app.py`)

```python
# Tested with fastapi.testclient.TestClient
Ran 5 tests in 0.031s
OK
```

- `test_root_endpoint`: Verifies API online status and docs route.
- `test_create_and_get_todo`: Verifies 201 Created status, ID allocation, and field validation.
- `test_update_todo_status`: Verifies partial PATCH updates.
- `test_list_and_filter_todos`: Verifies query parameter filtering (`?completed=true`) and pagination.
- `test_delete_todo`: Verifies 204 No Content response and subsequent 404 lookup.

---

## 5. Submission Summary

```text
================================================================================
     EXERCISE SUBMISSION: LEARN A NEW FRAMEWORK / LIBRARY / API (FASTAPI)
================================================================================
Student: Talifhani
Language & Framework: Python 3.11+ / FastAPI
Target Module: learning-with-ai/frameworks-fastapi/python/

1. ARCHITECTURAL HIGHLIGHTS:
   - Built a complete CRUD RESTful API using FastAPI & Pydantic models.
   - Applied Dependency Injection (Depends) for request-scoped context.
   - Built contextual translation guides bridging Flask/Django to FastAPI.

2. EMPIRICAL VERIFICATION:
   - 5 automated unit tests executed via TestClient: 100% passing (OK).
================================================================================
```
