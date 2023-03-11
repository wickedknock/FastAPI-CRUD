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


@router.post("/")
