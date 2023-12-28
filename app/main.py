from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from . import model

# import .

from sqlalchemy.orm import Session
from .Database import engine, SessionLocal

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True


my_posts = [
    {
        "ID": 1,
        "title": "Title 1",
        "content": "Post Content 1"
    },
    {
        "ID": 2,
        "title": "Title 2",
        "content": "Post Content 2"
    }
]

@app.get("/sqlalchemy")
def sql(db: Session = Depends(get_db) ):
    pass
 
@app.get("/")
def index():
    return {"message": "Welcome"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

def find_post(id):
    for post in my_posts:
        if id == post["ID"]:
            return post

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )

    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post.dict()
    new_post["ID"] = randrange(0, 10000) 
    my_posts.append(new_post)
    return {"data": new_post}

def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post["ID"] == id:
            return i

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_post_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id:int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )
    my_post = post.dict()
    my_post["ID"] = id
    my_posts[index] = my_post
    return {"message": "Post updated successfully"}