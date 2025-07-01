from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.schemas.jwt_token import Token
from app.schemas.user import UserFilter
from app.crud import user as user_curd
from app.db.database import get_db


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing accept token")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token = Token(**payload)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Ivalide token")

    user = user_curd.get_user(db, UserFilter(username=token.sub))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    user = user[0]
    return user
