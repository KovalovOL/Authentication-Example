from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models import User as UserDB
from app.schemas import user as user_schemes
from app.core.security import hash_password



def get_user(db: Session, data: user_schemes.UserFilter):
    conditions = []

    if data.id is not None: conditions.append(UserDB.id == data.id)
    if data.username is not None: conditions.append(UserDB.username == data.username)

    return db.query(UserDB).filter(*conditions).all()

def create_user(db: Session, user: user_schemes.CreateUser):
    new_user = UserDB(
        username = user.username,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def delete_user(db: Session, user_id: int):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    db.delete(user)
    db.commit()
    return user

def update_user(db: Session, user_id: int, data: user_schemes.UpdateUser):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User woth id {user_id} not found")

    if data.username is not None: user.username = data.username
    if data.password is not None: user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return user