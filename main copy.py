from typing import Optional
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel

from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from blog import schema
from blog import models

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables in the database
# models.metadata.create_all(bind=engine)


models.Base.metadata.create_all(bind=engine)


@app.get("/blog/unpublished")
async def get_unpublished_blogs():
    return {"data": "This is unpublished blog data"}


@app.get("/blog")
async def index(limit: int, published: Optional[bool] = True,
                sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}
    if not published:
        return {"data": f"{limit} unpublished blogs from the db"}


@app.get("/blog/{id}")
async def get_blog(id: int):
    return {"data": id}


class Blog(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

@app.post("/blog")
async def create_blog(request: Blog):
    return {"data": f"Blog is created with title {request.title} \
                    and content {request.content}, \
                    published: {request.published}, \
                    rating: {request.rating}"}


@app.post("/blogcreate", status_code=status.HTTP_201_CREATED)
async def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        content=request.content,
        published=request.published,
        rating=request.rating
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    # db.add(new_blog)  # Add the new blog to the session
    # db.commit()  # Commit the session to save the blog to the database
    # db.refresh(new_blog)  # Refresh the instance to get the updated
    # data from the database
    # return new_blog
    return schema.Blog.model_validate(new_blog)  # Use model_validate


@app.get("/createblog")
async def get_all_blog_data(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog    


@app.get("/createblog/{id}")
async def show_blog_by_id(id: int, response: Response,
                          db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog with {id} not found"}
    return blog


@app.delete("/createblog/{id}")
async def delete_blog_by_id(id: int, response: Response,
                            db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id: {id} not found")
    db.delete(blog)
    db.commit()
    return {"message": f"Blog with id : {id}deleted successfully"}


@app.put("/createblog/{id}")
async def update_blog_by_id(id: int, request: schema.Blog,
                            db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id: {id} not found")
    blog.title = request.title
    blog.content = request.content
    blog.published = request.published
    blog.rating = request.rating
    db.commit()
    db.refresh(blog)
    return blog