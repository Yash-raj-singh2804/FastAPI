from fastapi import APIRouter, Depends, Response, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models
from .oauth2 import get_current_user


router = APIRouter(
    prefix="/blogs",   
    tags=["blogs"]
    )

get_db = database.get_db

@router.get('', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db : Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/{id}', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id: int ,response: Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    return blog

@router.delete('/{id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def delete(id: int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")
    db.commit()
    return {'message' : f'Blog with id {id} deleted'}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: schemas.Blog, db : Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")
    blog = blog_query.update({'title' : request.title})
    db.commit()
    return {'detail' : f'Title updated to {request.title}'}


