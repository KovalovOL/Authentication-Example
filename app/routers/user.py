from fastapi import APIRouter, Depends, Path, Query, Response, Request, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.user import *
from app.db.database import get_db
from app.crud import user as user_crud
from app.core.security import create_access_token
from app.core.dependencies import get_current_user


router = APIRouter()


@router.get("/")
async def get_user(
    user_id: int = Query(None, ge=1),
    username: str = Query(None, min_length=4, max_length=50),
    db: Session = Depends(get_db)
):

    filter = UserFilter(
        id = user_id,
        username=username
    )

    return user_crud.get_user(db, filter)

@router.post("/")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    return {"message": f"You can create new user via registration"}
    # return user_crud.create_user(db, user)

@router.put("/")
async def update_user(
    response: Response,
    updates: UpdateUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    "Update a currect user"

    updated_user = user_crud.update_user(db, current_user.id, updates)
    response.set_cookie(key="access_token", value=create_access_token({"sub": updated_user.username}), httponly=True)
    return updated_user


@router.delete("/")
async def delete_user(
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    "Delete a currect user"

    deleted_user = user_crud.delete_user(db, current_user.id)
    response.delete_cookie("access_token")
    return {"message": f"User {deleted_user.username} has been deleted"}