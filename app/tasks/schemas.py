from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBaseSerializer(BaseModel):
    title: str = Field(..., 
                       max_length=150, 
                       description='This is the topic or header of each task', 
                       examples=['Watch movie'])
    description: Optional[str] = Field(None, 
                                       max_length=500, 
                                       description='Description of the task',
                                       examples=['Watch SpiderMan 2 from 2001'])
    is_completed: bool = Field(..., description='state of the task')

class TasksSerializer(TaskBaseSerializer):
    pass

class TasksResponseSerializer(TaskBaseSerializer):
    id: int = Field(..., description='Unique identifier of the object')
    created_date: datetime = Field(..., description='Creating date and time of the object')
    updated_date: datetime = Field(..., description='Updating date and time of the object')