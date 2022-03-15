from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import UUID4
from app.config import settings
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.models import User
from app import schemas

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["userID"] = str(to_encode["userID"])
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRECT_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    # sourcery skip: inline-immediately-returned-variable
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invaild Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credentialsException)
    user = db.query(User).filter(User.id == token.id).first()
    return user


def verify_access_token(token: str, credentialsException):
    try:
        payload = jwt.decode(token, settings.SECRECT_KEY,
                             algorithms=[settings.ALGORITHM])
        id: UUID4 = payload.get("userID")
        expires = payload.get("exp")

        if id is None:
            raise credentialsException

        tokenData = schemas.TokenData(id=id, expires=expires)

        if expires is None:
            raise credentialsException

        if tokenData.expires.replace(tzinfo=None) < datetime.utcnow():
            raise credentialsException

    except JWTError as e:
        raise credentialsException from e

    return tokenData
