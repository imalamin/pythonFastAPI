from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

    class Config:
        from_attributes = True  # Enable SQLAlchemy-to-Pydantic conversion