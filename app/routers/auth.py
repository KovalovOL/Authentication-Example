from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schemas.user import *
from app.core.dependencies import get_current_user
from app.core.security import verify_password, create_access_token
from app.crud import user as user_crud
from app.db.database import get_db


router = APIRouter()


@router.post("/register")
async def register_user(user_data: CreateUser, db: Session = Depends(get_db)):
    if user_crud.get_user(db, UserFilter(username=user_data.username)):
        raise HTTPException(status_code=409, detail="Such user already exists")

    new_user = user_crud.create_user(db, user_data)
    return {"message": f"User {new_user.username} has been created"}


@router.post("/login")
async def login_user(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, UserFilter(username=credentials.username))

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    user = user[0]

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password or username is incorrect")
    
    token = create_access_token({"sub": user.username})
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Login successful"}


@router.get("/me")
async def get_current_user_via_cookie(current_user = Depends(get_current_user)):
    return {"username": current_user.username}