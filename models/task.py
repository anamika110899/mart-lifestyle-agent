# models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    is_done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
