from fastapi import APIRouter, Depends, HTTPException ,status
from sqlalchemy.orm import Session
import schemas
from database import get_db
import models
from hashing import Hash
from tokens import Token

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
def register(request:schemas.Register,db:Session = Depends(get_db)):
    password = Hash.get_password_hash(request.password)
    user_instance = models.User(email = request.email, name = request.name,password = password)
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance

@router.post("/login")

def login(request: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    if not Hash.verify_password(request.password,user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")

    access_token = Token.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}