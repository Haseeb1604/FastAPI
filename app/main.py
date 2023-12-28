from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

from sqlalchemy.orm import Session
from . import models
from .Database import engine, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts