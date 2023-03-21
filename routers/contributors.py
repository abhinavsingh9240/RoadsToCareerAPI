from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from oauth2 import OAuth2
from operations.contributor_ops import ContributorOps
from typing import List,Optional
router = APIRouter(
    prefix="/contributor",
    tags=["Contributors"],
)

"""
    Routes for contributor
    
    GET /contributor           -> Return the contributor's basic information
    GET /contributor/courses   -> Return the contrubutor's Course List
    GET /contributor/roles     -> Return the contributor's roles list
    GET /contributor/skills    -> Return the contributos's skills list

    GET /contributor/{id}           -> Return the contributor's basic information
    GET /contributor/{id}/courses   -> Return the contrubutor's Course List
    GET /contributor/{id}/roles     -> Return the contributor's roles list
    GET /contributor/{id}/skills    -> Return the contributos's skills list

    PUT /contributor/description   -> To update the contributor description
"""

@router.get("")
def get_contributor_profile(user_id:int = Depends(OAuth2.get_current_user),db:Session = Depends(get_db)):

    return ContributorOps.get_contributor_profile(user_id,db)

@router.get("/courses",response_model=List[schemas.Base])
def get_contributor_profile(user_id:int = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_courses(user_id,db)

@router.get("/roles",response_model=List[schemas.Base])
def get_contributor_profile(user_id:int = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_roles(user_id,db)

@router.get("/courses",response_model=List[schemas.Base])
def get_contributor_profile(user_id:int = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_skills(user_id,db)

@router.put("/description")
def update_description(request:schemas.UpdateContribDesc,user_id:int = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.update_description(request.desc,user_id,db)

@router.get("{id}")
def get_contributor_profile_by_id(id:int,db:Session = Depends(get_db)):
    return ContributorOps.get_contributor_profile(id,db)

@router.get("/{id}/courses",response_model=List[schemas.Base])
def get_contributor_profile_by_id(id:int,db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_courses(id,db)

@router.get("/{id}/roles",response_model=List[schemas.Base])
def get_contributor_profile_by_id(id:int,db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_roles(id,db)

@router.get("/{id}/courses",response_model=List[schemas.Base])
def get_contributor_profile_by_id(id:int,db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_skills(id,db)

