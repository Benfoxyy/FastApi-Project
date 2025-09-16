from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., title="Title of the task", max_length=100)
    description: Optional[str] = Field(default=None, title="Description of the task", max_length=300)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int = Field(..., title="ID of the task")
    model_config = ConfigDict(from_attributes=True)