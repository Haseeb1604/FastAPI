from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
# from typing import Optional, List

# from sqlalchemy.orm import Session

from . import models, schema, utils
from .Database import engine, get_db
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
