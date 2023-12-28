from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional
from random import randrange

from sqlalchemy.orm import Session

from . import models, schema
from .Database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": "my_posts"}

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )

    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schema.Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict()
        )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post: schema.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    my_post = post_query.first()
    if my_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}