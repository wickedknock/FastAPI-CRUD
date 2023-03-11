
from typing import Dict, List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import models, oauth2, schema
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@ router.get("/", response_model=List[schema.PostResponse])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return posts


@router.get("/{id}", response_model=schema.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        HTTPException(status.HTTP_404_NOT_FOUND, "not found ")
    print(post)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(post: schema.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    # post.owner_id = user_id.id
    # new_post = models.Post(
    # owner_id=user_id.id, **post.dict())
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found ")

    if post.first().owner_id != user_id.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "not authorized to delete")

    post.delete(synchronize_session=False)
    db.commit()
    return 0


@ router.put("/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: schema.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_updated = post_query.first()

    if post_updated == None:
        HTTPException(status.HTTP_404_NOT_FOUND, "not found ")

    if post_updated.owner_id != user_id.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "not authorized to update ")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
