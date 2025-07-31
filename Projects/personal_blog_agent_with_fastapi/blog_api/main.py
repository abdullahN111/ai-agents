from fastapi import FastAPI
from .blogs.main import router as blog_router
from fastapi import FastAPI
from utils import models, database

app = FastAPI()

models.Base.metadata.create_all(database.engine)
app.include_router(blog_router, prefix="/blogs", tags=["Blogs"])


@app.get("/")
async def root():
    return {"message": "Welcome to Personal Blog API!"}
