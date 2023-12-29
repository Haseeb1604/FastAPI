from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import schema, models
from . import oauth2
from ..Database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schema.Post])
def get_posts(
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
    ):
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}", response_model=schema.Post)
def get_post(
    id: int, response: Response, 
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
    ):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )

    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(
    post: schema.PostCreate, 
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
    ):
    
    new_post = models.Post(
        **post.dict()
        )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id:int, 
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(
    id:int, post: schema.PostCreate, 
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    my_post = post_query.first()
    if my_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} not found"
            )
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()