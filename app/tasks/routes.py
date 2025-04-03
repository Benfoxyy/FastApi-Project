from fastapi import APIRouter, status, HTTPException, Depends, Query, Path
from fastapi.responses import JSONResponse
from tasks.schemas import TasksSerializer, TasksResponseSerializer
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List, Optional
from tasks.models import TaskModel

router = APIRouter(tags=['Tasks'], prefix='/task')

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TasksResponseSerializer])
def GetTasks(title:Optional[str] = Query(None, max_length=20),
            is_completed:Optional[bool] = Query(None),
            db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if title:
        query = query.filter(TaskModel.title.ilike(f"%{title}%"))
    if is_completed is not None:
        query = query.filter_by(is_completed = is_completed)
    return query.all() 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TasksResponseSerializer)
def CreateTask(request: TasksSerializer, db: Session = Depends(get_db)):
    task = TaskModel(**request.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put('/{task_id}', status_code=status.HTTP_202_ACCEPTED, response_model=TasksResponseSerializer)
def UpdateTask(request: TasksSerializer, task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter_by(id = task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object Not Found')
    task.title = request.title
    task.description = request.description
    task.is_completed = request.is_completed
    print(request.model_dump())
    db.commit()
    db.refresh(task)
    return task

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def DeleteTask(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object Not Found')
    db.delete(task)
    db.commit()