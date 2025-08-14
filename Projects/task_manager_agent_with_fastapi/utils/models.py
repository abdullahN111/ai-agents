from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from utils.database import Base, SessionLocal



class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    deadline = Column(String)


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: str

class TaskCreate(TaskBase):
    """For incoming POST request body"""
    pass

class TaskModel(TaskBase):
    id: int
    
    class Config:
        from_attributes = True
        

        
def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        