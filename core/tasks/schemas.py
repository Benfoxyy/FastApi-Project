from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=100, description="Tasks main title")
    description: Optional[str] = Field(
        None, max_length=500, description="Tasks description"
    )
    is_completed: bool = Field(False, description="Tasks status")


class TaskReadSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique identifier of tasks")
    created_date: datetime = Field(
        ..., description="Exact time that task has been created"
    )
    model_config = ConfigDict(from_attributes=True)


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass
