from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from oauth2 import OAuth2
import schemas
from database import get_db
from operations.skill_ops import SkillOps

router = APIRouter(
    prefix="/skill",
    tags=["Skills"]
)


@router.post("/")
def post_skill(skill:schemas.Skill, db:Session = Depends(get_db),email:str = Depends(OAuth2.get_current_user)):
    return SkillOps.add_skill(db=db,skill=skill,email = email)

@router.get("/")
def get_skill(db:Session = Depends(get_db)):
    return SkillOps.show_skill_all(db=db)

@router.get("/{id}")
def get_skill_by_id(id:int,db:Session = Depends(get_db)):
    return SkillOps.show_skill_id(id,db)

@router.get("/search/{query}")
def get_skill_by_name(query:str,db:Session = Depends(get_db)):
    return SkillOps.skill_search(query,db)

@router.delete("/{id}")
def remove_skill(id:int, db:Session=Depends(get_db),email:str = Depends(OAuth2.get_current_user)):
    
    SkillOps.remove(id,db,email = email)
    return {"done"}

@router.put("/{id}")
def update_skill(id:int,request:schemas.Skill,db:Session=Depends(get_db),email:str = Depends(OAuth2.get_current_user)):
    SkillOps.update(id,request,db,email = email)
    return {"Done"}