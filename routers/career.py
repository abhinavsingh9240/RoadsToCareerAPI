from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
import schemas
from database import get_db
from operations.career_ops import CareerOps

from oauth2 import OAuth2

router = APIRouter(
    prefix="/career",
    tags=["Career"]
)

@router.post("/")
def post_career(career: schemas.Career, db:Session = Depends(get_db)):
    return CareerOps.add_career(db = db, career=career)

@router.get("/")
def get_career(db:Session = Depends(get_db),current_user:schemas.User = Depends(OAuth2.get_current_user)):
    return CareerOps.show_career_all(db=db)

@router.get("/{id}")
def get_career_by_id(id:int,db:Session = Depends(get_db)):
    return CareerOps.show_career_id(id,db)


@router.get("/search/{query}")
def get_career_by_name(query:str,db:Session = Depends(get_db)):
    return CareerOps.career_search(query,db)

@router.delete("/{id}")
def remove_career(id:int,db:Session = Depends(get_db)):
    CareerOps.remove(id,db)
    return {"Done"}

@router.put("/{id}")
def update_career(id,request:schemas.Career,db:Session = Depends(get_db)):
    CareerOps.update(id,request,db)
    return {"Done"}