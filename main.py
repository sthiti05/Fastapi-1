from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
import schemas,model
from database import Base,engine,SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash 


app=FastAPI()

model.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blog'])
def create(request:schemas.Blog, db:Session= Depends(get_db)):
    new_blog = model.Blog(title=request.title,body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog/{id}',response_model=schemas.ShowBlog,tags=['blog'])
def show(id,response=Response,db: Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'The blog with id {id} is not available'}
    return blog

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def update(id,request:schemas.Blog, db:Session= Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Blog with id {id} not found")
    blog.update(request.model_dump())
    db.commit()
    return 'updated'

@app.delete('/blog/{id}',status_code = status.HTTP_204_NO_CONTENT,tags=['blog'])
def destroy(id,db:Session = Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Blog with id {id} not found")
    blog.delete(synchronize_session = False)
    db.commit()
    return 'done'

@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blog'])
def all(db: Session=Depends(get_db)):
    blogs=db.query(model.Blog).all()
    return blogs


@app.post('/user',response_model=schemas.ShowUser,tags=['users'])
def create_user(request:schemas.User,db: Session=Depends(get_db)):
    new_user = model.User(name=request.name,email = request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['users'])
def show(id=int,db: Session=Depends(get_db)):
    user=db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user with id {id} is not available")
       
    return user