from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List


from app import models, oauth2, schemas
from app.database import engine, get_db


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


@router.get("/", response_model=List[schemas.ResponsePost])
def get_posts(db: Session = Depends(get_db), 
              skip: int = 0, 
              limit: int = 100, 
              current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts


@router.get("/{id}", response_model=schemas.ResponsePost)
def get_post_by_id(id: int, 
                   db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.CreatePost, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponsePost)
def update_post(id: int, 
                updated_post: schemas.PostBase, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()
