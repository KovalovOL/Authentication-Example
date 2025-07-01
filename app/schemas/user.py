from pydantic import BaseModel, Field
from typing import Optional


class CreateUser(BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)

class UserLogin(CreateUser):
    ...

class User(CreateUser):
    id: int

class UserFilter(BaseModel):
    id: Optional[int] = Field(None, ge=0)
    username: Optional[str] = Field(None, min_length=4, max_length=50)

class UpdateUser(BaseModel):
    username: Optional[str] = Field(None, min_length=4, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=50)