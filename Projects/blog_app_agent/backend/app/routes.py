import os
import shutil
from typing import List
import uuid
from fastapi import APIRouter, File, Form, HTTPException, Depends, UploadFile, status
from sqlalchemy.orm import Session
from utils import models
from utils.database import engine
from typing import Annotated
from utils.auth import get_current_user  

db_dependency = Annotated[Session, Depends(models.get_db)]
models.Base.metadata.create_all(bind=engine)

router = APIRouter()




@router.post("/blogs", response_model=models.BlogModel)
async def create_blog(blog: models.BlogCreate, db: db_dependency):
    slug = blog.title.lower().replace(" ", "-") 

    new_blog = models.Blog(
        title=blog.title,
        slug=slug,
        perspective=blog.perspective,
        content=blog.content,
        category=blog.category.lower(),
        popularity=blog.popularity,
        primary_image=blog.primary_image,
        secondary_image=blog.secondary_image,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.post("/upload-images")
async def upload_images(
    primary_image: UploadFile = File(...),
    secondary_image: UploadFile = File(None)
):
   
    primary_filename = f"{uuid.uuid4().hex}_{primary_image.filename}"
    primary_path = os.path.join("static", primary_filename)
    
    with open(primary_path, "wb") as buffer:
        shutil.copyfileobj(primary_image.file, buffer)
    

    secondary_path = None
    if secondary_image:
        secondary_filename = f"{uuid.uuid4().hex}_{secondary_image.filename}"
        secondary_path = os.path.join("static", secondary_filename)
        
        with open(secondary_path, "wb") as buffer:
            shutil.copyfileobj(secondary_image.file, buffer)
    
    return {
        "primary": primary_path,
        "secondary": secondary_path
    }
    
@router.get("/blogs", response_model=List[models.BlogModel])
async def get_all_blogs(db: db_dependency):
    return db.query(models.Blog).all()

@router.get("/blogs/{slug}", response_model=models.BlogModel)
async def get_single_blog(slug: str, db: db_dependency):
    blog = db.query(models.Blog).filter(models.Blog.slug == slug).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.get("/blogs/category/{category}", response_model=List[models.BlogModel])
async def get_single_blog(category: str, db: db_dependency):
    blog = db.query(models.Blog).filter(models.Blog.category == category.lower()).all()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.post("/comments", response_model=models.CommentModel)
async def add_comment(comment: models.CommentCreate, db: db_dependency, user: models.User = Depends(get_current_user)):
    new_comment = models.Comment(
        blog_id=comment.blog_id,
        user_id=user.id,
        text=comment.text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/blogs/{blog_id}/comments", response_model=List[models.CommentWithUser])
async def get_comments_for_blog(blog_id: int, db: db_dependency):
    comments = (
        db.query(models.Comment)
        .filter(models.Comment.blog_id == blog_id)
        .order_by(models.Comment.created_at.desc())
        .all()
    )

    return [
        models.CommentWithUser(
            id=c.id,
            blog_id=c.blog_id,
            text=c.text,
            created_at=c.created_at,
            user_id=c.user_id,
            user_name=c.user.name if c.user else "Anonymous"
        )
        for c in comments
    ]
