from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import List
from tasks.schemas import *
from sqlalchemy.orm import Session
from config.database import get_db
from tasks.models import TaskModel

router = APIRouter(tags=["tasks"])

@router.get("/", response_model=List[TaskReadSchema])
def read_task(db: Session = Depends(get_db)):
    query = db.query(TaskModel).all()
    return query

@router.post("/", response_model=TaskReadSchema)
def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    data = request.model_dump()
    task_obj = TaskModel(**data)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    
    return task_obj

@router.put("/{task_id}", response_model=TaskReadSchema)
def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(detail="Task with this ID has not existed", status_code=status.HTTP_404_NOT_FOUND)
    
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)
    
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int = Path(...), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(detail="Task with this ID has not existed", status_code=status.HTTP_404_NOT_FOUND)
    db.delete(task_obj)
    db.commit()