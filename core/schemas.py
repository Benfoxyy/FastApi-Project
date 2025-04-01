from pydantic import BaseModel, Field
from datetime import datetime

class TasksSerializer(BaseModel):
    title: str
    description: str = None
    is_done: bool = Field(default=False)
    # created_date: datetime

class TasksResponseSerializer(BaseModel):
    id: int
    title: str
    description: str = None
    is_done: bool = Field(default=False)
    # created_date: datetime

    class Config:
        orm_mode = True