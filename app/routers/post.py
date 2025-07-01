from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.schemas.post import *
from app.schemas.user import User
from app.crud import post as post_crud
from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/")
async def get_post(
    title: str = Query(None, min_length=3, max_length=25),
    owner_id: int = Query(None, ge=0),
    time_created: datetime = Query(None),
    db: Session = Depends(get_db)
):

    filter = PostFilter(
        title=title,
        owner_id=owner_id,
        time_created=time_created
    )

    return post_crud.get_post(db, filter)

@router.post("/")
async def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    post.owner_id = current_user.id
    return post_crud.create_post(db, post)

@router.put("/{post_id}")
async def update_post(
    updates: UpdatePost,
    post_id: int = Path(..., ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    post = post_crud.get_post(db, PostFilter(post_id=post_id))
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    post = post[0]

    post_owner_id = post.owner_id
    if post_owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can't change other user's posts")

    return post_crud.update_post(db, post_id, updates)

@router.delete("/{post_id}")
async def delete_post(  
    post_id: int = Path(..., ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    post = post_crud.get_post(db, PostFilter(post_id=post_id))
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    post = post[0]

    post_owner_id = post.owner_id
    if post_owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can't change other user's posts")

    return post_crud.delete_post(db, post_id)