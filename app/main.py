from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, post, user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get('/')
def root():
    return {"msg": "hello"}


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
