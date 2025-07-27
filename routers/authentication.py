from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from hashing import Hash
import model, schemas,database

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(request:schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return user