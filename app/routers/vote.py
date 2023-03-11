import json
from typing import Dict, List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import models, oauth2, schema
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == user_id.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status.HTTP_409_CONFLICT, f'user {user_id.id} has already liked the post with id {vote.post_id}')
        new_vote = models.Votes(post_id=vote.post_id, user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        return {"message": "added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f"vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "removed vote"}
