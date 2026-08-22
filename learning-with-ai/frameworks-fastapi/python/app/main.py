from fastapi import FastAPI, HTTPException, Query, Path, status, Depends
from typing import List, Optional
from datetime import datetime
from .models import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(
    title="FastAPI Todo API",
    description="Learning new frameworks: A robust FastAPI application with dependency injection, validation, and CRUD operations.",
    version="1.0.0"
)

# In-memory database repository
todos_db = {}
id_counter = 0


def get_current_timestamp() -> str:
    return datetime.utcnow().isoformat()


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Learning API",
        "docs_url": "/docs",
        "status": "online"
    }


@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, timestamp: str = Depends(get_current_timestamp)):
    global id_counter
    id_counter += 1
    # Unpack model data
    todo_dict = todo.model_dump() if hasattr(todo, "model_dump") else todo.dict()
    new_todo = {
        "id": id_counter,
        **todo_dict,
        "created_at": timestamp
    }
    todos_db[id_counter] = new_todo
    return new_todo


@app.get("/todos/", response_model=List[TodoResponse])
async def list_todos(
    completed: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    items = list(todos_db.values())
    if completed is not None:
        items = [t for t in items if t["completed"] == completed]
    return items[skip:skip + limit]


@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int = Path(..., gt=0)):
    if todo_id not in todos_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo #{todo_id} not found")
    return todos_db[todo_id]


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, updates: TodoUpdate):
    if todo_id not in todos_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo #{todo_id} not found")
    
    current = todos_db[todo_id]
    update_data = updates.model_dump(exclude_unset=True) if hasattr(updates, "model_dump") else updates.dict(exclude_unset=True)
    current.update(update_data)
    todos_db[todo_id] = current
    return current


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo #{todo_id} not found")
    del todos_db[todo_id]
    return None
