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

@router.post("/{id}/promote")
def promote_user(id:int,db:Session = Depends(get_db)):
    return ContributorOps.promote(user_id=id,db=db)

@router.post("/{id}/demote")
def demote_user(id:int,db:Session = Depends(get_db)):
    return ContributorOps.demote(id,db)

@router.get("",response_model=schemas.ContributorResponse)
def get_contributor_profile(email:str = Depends(OAuth2.get_current_user),db:Session = Depends(get_db)):
    return ContributorOps.get_contributor_profile(email=email,db = db)

@router.get("/courses",response_model=List[schemas.Base])
def get_contributor_courses(email:str = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_courses(email=email,db = db)

@router.get("/roles",response_model=List[schemas.Base])
def get_contributor_roles(email:str = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_roles(email=email,db = db)

@router.get("/skills",response_model=List[schemas.Base])
def get_contributor_skills(email:str = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_skills(email=email,db = db)

@router.put("/description")
def update_description(request:schemas.UpdateContribDesc,email:str = Depends(OAuth2.get_current_user),db:Session=Depends(get_db)):
    return ContributorOps.update_description(newdesc = request.desc,email = email,db = db)

@router.get("/{id}",response_model=schemas.ContributorResponse)
def get_contributor_profile_by_id(id:int,db:Session = Depends(get_db)):
    return ContributorOps.get_contributor_profile(db = db,id = id)

@router.get("/{id}/courses",response_model=List[schemas.Base])
def get_contributor_course_by_id(id:int,db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_courses(db = db,id = id)

@router.get("/{id}/roles",response_model=List[schemas.Base])
def get_contributor_roles_by_id(id:int,db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_roles(db = db,id = id)

@router.get("/{id}/skills",response_model=List[schemas.Base])
def get_contributor_skills_by_id(id:int,db:Session=Depends(get_db)):
    return ContributorOps.get_contributor_skills(db = db,id = id)


