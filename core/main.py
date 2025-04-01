from fastapi import FastAPI, status, HTTPException, Depends, Query
from contextlib import asynccontextmanager
from schemas import TasksSerializer, TasksResponseSerializer
from sqlalchemy.orm import Session
from database import Base, engine, get_db, Task
from typing import List, Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI is starting")

    yield

    print("FastAPI is down")

app = FastAPI(lifespan=lifespan)


@app.get("/", status_code=status.HTTP_200_OK, response_model=List[TasksResponseSerializer])
def GetTasks(title:Optional[str] = Query(None, max_length=20),
            is_done:Optional[bool] = Query(None),
            db: Session = Depends(get_db)):
    query = db.query(Task)
    if title:
        query = query.filter(Task.title.ilike(f"%{title}%"))
    if is_done is not None:
        query = query.filter(Task.is_done == is_done)
    return query.all() 

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=TasksResponseSerializer)
def CreateTask(request: TasksSerializer, db: Session = Depends(get_db)):
    task = Task(
        title=request.title,
        description =request.description
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.put('/{task_id}', status_code=status.HTTP_202_ACCEPTED, response_model=TasksResponseSerializer)
def UpdateTask(task_id: int, request: TasksSerializer, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object Not Found')
    task.title = request.title
    task.description = request.description
    task.is_done = request.is_done
    db.commit()
    db.refresh(task)
    return task

@app.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def DeleteTask(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object Not Found')
    db.delete(task)
    db.commit()