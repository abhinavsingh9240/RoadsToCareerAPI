from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
import schemas
from database import get_db
from operations.role_ops import RoleOps

from oauth2 import OAuth2

router = APIRouter(
    prefix="/role",
    tags=["Role"]
)

@router.post("/")
def post_career(career: schemas.RoleBase, db:Session = Depends(get_db),email:str = Depends(OAuth2.get_current_user)):
    return RoleOps.add(db = db, career=career,email = email)

@router.get("/")
def get_career(db:Session = Depends(get_db)):
    return RoleOps.show_role_all(db=db)

@router.get("/{id}")
def get_career_by_id(id:int,db:Session = Depends(get_db)):
    return RoleOps.show_role_id(id,db)


@router.get("/search/{query}")
def get_career_by_name(query:str,db:Session = Depends(get_db)):
    return RoleOps.career_search(query,db)

@router.delete("/{id}")
def remove_career(id:int,db:Session = Depends(get_db),email:str = Depends(OAuth2.get_current_user)):
    RoleOps.remove(id,db,email)
    return {"Done"}

@router.put("/{id}")
def update_career(id,request:schemas.RoleBase,db:Session = Depends(get_db),email:str = Depends(OAuth2.get_current_user)):
    RoleOps.update(id,request,db,email)
    return {"Done"}