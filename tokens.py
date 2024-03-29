from datetime import datetime, timedelta
from jose import jwt, JWTError
import models
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session

class Token:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 36000

    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=Token.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Token.SECRET_KEY, algorithm=Token.ALGORITHM)
        return encoded_jwt
    
    def verify_token(token:str,credentials_exception):
        try:
            payload = jwt.decode(token, Token.SECRET_KEY, algorithms=[Token.ALGORITHM])
            email: str = payload.get("sub")
            
            if email is None:
                raise credentials_exception
            return email
        except JWTError as e:
            print(e)
            raise credentials_exception
        
    