from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreatePost(BaseModel):
    title: str = Field(..., min_length=3, max_length=25)
    text: Optional[str] = Field(None)
    owner_id: int = Field(..., ge=0)

class Post(CreatePost):
    id: int = Field(..., ge=0)
    time_created: datetime

class PostFilter(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=25)
    owner_id: Optional[int] = Field(None, ge=0)
    time_created: Optional[datetime]
    post_id: Optional[int] = Field(None, ge=0)

class UpdatePost(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=25)
    text: Optional[str]
    owner_id: Optional[int] = Field(None, ge=0)
