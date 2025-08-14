from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from utils import models
from utils.database import engine
from typing import Annotated

db_dependency = Annotated[Session, Depends(models.get_db)]
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/tasks", response_model=models.TaskModel, status_code=status.HTTP_201_CREATED)
async def create_task(task: models.TaskModel, db: db_dependency):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/tasks", response_model=List[models.TaskModel])
async def get_all_tasks(db: db_dependency):
    return db.query(models.Task).all()

@router.get("/tasks/{id}", response_model=models.TaskModel)
async def get_single_task(id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
