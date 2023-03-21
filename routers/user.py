from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from oauth2 import OAuth2
from operations.user_ops import UserOps
from typing import List,Optional
router = APIRouter(
    prefix="/user",
    tags=["Users"],
)

"""
    Routes for user:
    GET /user/profile       ->  profile of current user
    GET /user/courses  -> to get the list of liked courses
    GET /user/skills   -> to get the list of liked skills
    GET /user/roles    -> to get the list of liked roles
    
    PUT /user/name     -> to update the name of user
    PUT /user/email    -> to update the email of user
    PUT /user/password -> to update the password of user

"""
# TODO: Add the like functionality for user

@router.get("/profile/",response_model=schemas.UserBase)
def profile(email:str = Depends(OAuth2.get_current_user),db:Session = Depends(get_db)):
    response = UserOps.get_user(email,db)
    return response

@router.get("/courses",response_model=List[schemas.Base])
def get_liked_courses(limit:Optional[int] = None,email:str = Depends(OAuth2.get_current_user),db:Session = Depends(get_db)):
    if limit is None:
        response =  UserOps.liked_courses(email,db)
    else:
        response = UserOps.liked_courses(email,db)[:limit]
    
    return response

@router.get("/roles",response_model=List[schemas.Base])
def get_liked_roles(limit:Optional[int] = None,email:str = Depends(OAuth2.get_current_user),db:Session = Depends(get_db)):
    if limit is None:
        response = UserOps.liked_roles(email,db)
    else:
        response = UserOps.liked_roles(email,db)[:limit]
        
    return response

@router.get("/skills",response_model=List[schemas.Base])
def get_liked_skills(limit:Optional[int] = None,email:str = Depends(OAuth2.get_current_user),db:Session = Depends(get_db)):
    if limit is None:
        response = UserOps.liked_skills(email,db)
    else:
        response = UserOps.liked_skills(email,db)[:limit]
        
    return response

@router.put("/name")
def update_name(request:schemas.NameUpdate,
                email:str= Depends(OAuth2.get_current_user),
                db:Session = Depends(get_db)):
    return UserOps.update_name(request,email,db)

@router.put("/email")
def update_email(request:schemas.EmailUpdate,
                email:str = Depends(OAuth2.get_current_user),
                db:Session = Depends(get_db)):
    return UserOps.update_email(request,email,db)

@router.put("/password")
def update_password(request:schemas.PasswordUpdate,
                    email:str = Depends(OAuth2.get_current_user),
                    db:Session = Depends(get_db)):
    
    return UserOps.update_password(request,email)