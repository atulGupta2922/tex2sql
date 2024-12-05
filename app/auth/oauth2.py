from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta
import jwt
import os
from app.services.constants import const
from app.services.app_db import AppDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = const.app_secret
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    print(SECRET_KEY, to_encode)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={
            'WWW-Authenticate': 'Bearer'
        }
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id: str = payload.get('sub')
        print("USER ID: ",user_id)
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = AppDB().get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
  
def get_user_role_from_token(token: str):
  credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={
            'WWW-Authenticate': 'Bearer'
        }
    )
  try:
      payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
      role: str = payload.get('role')
      if role is None:
          raise credentials_exception
      return int(role)
  except Exception as e:
      raise e