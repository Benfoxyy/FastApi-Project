from fastapi import FastAPI, Depends, status, HTTPException
from database import Base, engine, get_db
from models import Task
from schemas import TaskCreate, TaskRead
from sqlalchemy.orm import Session
from typing import List

Base.metadata.create_all(bind=engine)
app = FastAPI(title="My API", version="1.0.0")

@app.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskRead])
def read_task(db: Session = Depends(get_db)):
    task = db.query(Task).all()
    return task

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskRead)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(task)
    db.commit()