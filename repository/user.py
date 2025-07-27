from sqlalchemy.orm import Session
import model,schemas
from fastapi import HTTPException,status
from hashing import Hash 

def create(request: schemas.User, db: Session):
    new_user = model.User(name=request.name,email = request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} is not available")
    return user