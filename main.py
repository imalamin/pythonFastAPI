# pythonFastAPI/main.py

from typing import Optional, List
from fastapi import Depends, FastAPI, Header
from pydantic import BaseModel

from book.database.b_database import engine, SessionLocal
from sqlalchemy.orm import Session
from book.database import b_schema, b_models

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables in the database
# models.metadata.create_all(bind=engine)


b_models.Base.metadata.create_all(bind=engine)


# ------------------------------- book sqlite --------------

@app.get('/books', response_model=List[b_schema.Book])
async def get_all_books(db: Session = Depends(get_db)):
    book_list = db.query(b_models.Book).all()
    return book_list












@app.get('/greet')
def greet(name: str, age: Optional[int] = 0) -> dict:
    return {"message": f" {name}", "age ": age}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }


@app.get('/get_headers', status_code=200)
async def get_header(
    accept: str = Header(),
    content_type: str = Header(),
    user_agent: str = Header(),
    host: str = Header()
):
    request_headers = {}

    request_headers["Accept"] = accept
    request_headers["Content-type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return {
        "accept": accept,
        "content_type": content_type,
        "user_agent": user_agent,
        "host": host
    }

