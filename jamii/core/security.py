from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

from jamii.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    userName: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz = timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes = 15)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(userName=username)
    
    except jwt.PyJWTError:
        raise credentials_exception
    



