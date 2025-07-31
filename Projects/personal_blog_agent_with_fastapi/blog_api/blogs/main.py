from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from utils import schemas, database
from blog_api.blogs import actions

router = APIRouter(
    prefix="/blogs",
    tags=['Blogs']
)


get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return actions.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return actions.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return actions.destroy(id,db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id:int, db: Session = Depends(get_db)):
    return actions.show(id,db)