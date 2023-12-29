from fastapi import FastAPI

from . import models
from .Database import engine
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
