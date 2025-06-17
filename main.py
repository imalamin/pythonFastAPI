from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel

from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from blog import schema
from blog import models

app = FastAPI()


@app.get('/greet')
def greet(name: str, age: Optional[int] = 0) -> dict:
    return {"message": f" {name}", "age ": age}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post('/create_book')
async def  create_book(book_data : BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }


@app.get('/get_headers', status_code=200)
async def get_header(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {}
    
    request_headers["Accept"] = accept
    request_headers["Content-type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    
    return request_headers