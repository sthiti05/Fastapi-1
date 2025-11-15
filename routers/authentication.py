from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash
import model, schemas,database,jwt_token
# from jwt_token import create_access_token


router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    

    access_token = jwt_token.create_access_token(data={"sub": user.email})
    return {"access_token" : access_token, "token_type":"bearer"}
    return user