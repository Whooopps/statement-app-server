from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import schemas, utils
from app.models import User
from app.database import get_db
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword

    newUser = User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: UUID4, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} Doesnt Exist")
    return user
