from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, util, oauth2
from ..database import get_db
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schema.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "not found")

    if not util.compare_password(user_cred.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "not found")

    jwt = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": jwt, "token_type": "bearer"}
