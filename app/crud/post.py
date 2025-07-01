from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.db.models import Post as PostDB
from app.schemas import post as post_schemes


def get_post(db: Session, data: post_schemes.PostFilter):
    conditions = []

    if data.title is not None: conditions.append(PostDB.title == data.title)
    if data.owner_id is not None: conditions.append(PostDB.owner_id == data.owner_id)
    if data.time_created is not None: conditions.append(PostDB.time_created >= data.time_created)
    if data.post_id is not None: conditions.append(PostDB.id == data.post_id)

    return db.query(PostDB).filter(*conditions).all()

def create_post(db: Session, post: post_schemes.CreatePost):
    new_post = PostDB(
        title = post.title,
        text = post.text,
        owner_id = post.owner_id,
        time_created = datetime.utcnow()
    )

    db.add(new_post)
    db.commit()
    return new_post

def update_post(db: Session, post_id:int, data: post_schemes.UpdatePost):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    if data.title is not None: post.title = data.title
    if data.text is not None: post.text = data.text
    if data.owner_id is not None: post.owner_id = data.owner_id
    post.time_created = datetime.utcnow()

    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    db.delete(post)
    db.commit()
    return post