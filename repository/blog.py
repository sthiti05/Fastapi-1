from sqlalchemy.orm import Session
import model,schemas
from fastapi import HTTPException,status    


def get_all(db:Session):
    blogs=db.query(model.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = model.Blog(title=request.title, body=request.body, user_id=1)  
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Blog with id {id} not found")
    blog.update(request.model_dump())
    db.commit()
    return 'updated'

def show(id: int, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} is not available")
    return blog