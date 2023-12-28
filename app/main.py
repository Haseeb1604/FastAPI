from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

from sqlalchemy.orm import Session
from . import models
from .Database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": "my_posts"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict()
        )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail= f"Post with id {id} not found"
#             )

#     return {"data": post}


# def find_post_index(id):
#     for i, post in enumerate(my_posts):
#         if post["ID"] == id:
#             return i

# @app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     index = find_post_index(id)
#     if not index:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail= f"Post with id {id} not found"
#             )

#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/post/{id}")
# def update_post(id:int, post: Post):
#     index = find_post_index(id)
#     if index == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail= f"Post with id {id} not found"
#             )
#     my_post = post.dict()
#     my_post["ID"] = id
#     my_posts[index] = my_post
#     return {"message": "Post updated successfully"}