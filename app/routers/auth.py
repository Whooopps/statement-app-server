from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils import OAuth2PasswordRequestJson
from sqlalchemy.orm import Session
from app import oauth2, schemas, utils
from app.database import get_db
from app.models import User
router = APIRouter()


@router.post("/api/checkemail")
async def check_email(data: schemas.CheckEmail, db: Session = Depends(get_db)):
    emailQuery = db.query(User).filter(User.email == data.email).first()
    if emailQuery is None:
        return {"valid": True}

    return {"valid": False}


@router.post("/api/login", response_model=schemas.Token)
async def login(userCredentilas: OAuth2PasswordRequestJson = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == userCredentilas.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invaild Email or Password")
    if not utils.verify(userCredentilas.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invaild Email or Password")
    accessToken = oauth2.create_access_token(data={"userID": user.id})

    return {
        "accessToken": accessToken,
        "tokenType": "bearer"
    }
