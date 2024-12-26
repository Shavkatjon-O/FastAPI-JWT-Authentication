from typing import Type

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import *
from database import get_db
from models import User
from oauth2 import bearer_security
from schemas import TokenData


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_security),
    db: Session = Depends(get_db),
) -> Type[User]:
    exception = HTTPException(
        status_code=404,
        detail="Not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token.credentials,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise exception
        token_data = TokenData(username=username)
    except JWTError:
        raise exception

    db_user = db.query(User).filter(User.username == token_data.username).first()

    if db_user is None:
        raise exception
    return db_user
