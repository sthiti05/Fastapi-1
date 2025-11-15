from fastapi import Depends, HTTPException, status
# from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt_token  # Assuming jwt_token is the module where the JWT functions are defined
from jwt_token import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
      credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
      token_data = verify_token(token, credentials_exception)
      return token_data 