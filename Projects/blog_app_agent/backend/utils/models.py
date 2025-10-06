from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from utils.database import Base, SessionLocal


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    perspective = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    popularity = Column(String, default="medium")
    primary_image = Column(String, nullable=True)   
    secondary_image = Column(String, nullable=True)   
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="comments")
    blog = relationship("Blog", backref="comments")



class BlogBase(BaseModel):
    title: str
    perspective: str
    content: Optional[str] = None
    category: str
    popularity: str = "medium"
    primary_image: Optional[str] = None
    secondary_image: Optional[str] = None


class BlogCreate(BlogBase):
    """For incoming POST request body"""
    pass


class BlogModel(BlogBase):
    id: int
    slug: str   
    created_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    blog_id: int
    text: str

class CommentCreate(CommentBase):
    pass

class CommentModel(CommentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CommentWithUser(CommentModel):
    user_name: str

    class Config:
        from_attributes = True




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


