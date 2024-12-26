from datetime import datetime, timedelta, timezone
from typing import Union

from jose import JWTError, jwt
from passlib.context import CryptContext

from config import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    result = None
    is_expired = False
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "verify_exp": False,
            },
        )
        expiration_time = datetime.fromtimestamp(payload["exp"])
        current_time = datetime.now()
        result = payload
        is_valid = all(key in payload for key in ["exp"])
        if expiration_time < current_time:
            is_expired = True
    except JWTError:
        is_valid = False
    return {
        "is_valid": is_valid,
        "is_expired": is_expired,
        "result": result,
    }
