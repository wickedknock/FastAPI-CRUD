from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, util
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd = util.hash(user.password)
    user.password = hashed_pwd

    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.UserOut])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    print(user)
    return user
