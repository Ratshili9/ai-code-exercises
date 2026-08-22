from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Optional detailed description")
    due_date: Optional[str] = Field(None, description="ISO formatted due date")
    completed: bool = Field(default=False, description="Completion status")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    created_at: str
