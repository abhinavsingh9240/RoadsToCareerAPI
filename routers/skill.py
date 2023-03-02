from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter(
    prefix="/skill",
    tags=["Skills"]
)


@router.post("/")
def post_skill(skill:schemas.skill, db:Session = Depends(get_db)):
    return crud.add_skill(db=db,skill=skill)

@router.get("/")
def get_skill(db:Session = Depends(get_db)):
    return crud.show_skill_all(db=db)

@router.get("/{id}")
def get_skill_by_id(id:int,db:Session = Depends(get_db)):
    return crud.show_skill_id(id,db)

@router.get("/search/{query}")
def get_skill_by_name(query:str,db:Session = Depends(get_db)):
    return crud.skill_search(query,db)