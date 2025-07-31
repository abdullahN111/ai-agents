from typing import Optional
from pydantic import BaseModel


class BlogBase(BaseModel):

    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    id: int
    title: str
    body: Optional[str]
    class Config():
        orm_mode = True



