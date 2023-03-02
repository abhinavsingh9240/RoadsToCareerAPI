from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
import schemas
from database import get_db
from operations.career_ops import CareerOps

router = APIRouter(
    prefix="/career",
    tags=["Career"]
)

@router.post("/")
def post_career(career: schemas.career, db:Session = Depends(get_db)):
    return CareerOps.add_career(db = db, career=career)

@router.get("/")
def get_career(db:Session = Depends(get_db)):
    return CareerOps.show_career_all(db=db)

@router.get("/{id}")
def get_career_by_id(id:int,db:Session = Depends(get_db)):
    return CareerOps.show_career_id(id,db)


@router.get("/search/{query}")
def get_career_by_name(query:str,db:Session = Depends(get_db)):
    return CareerOps.career_search(query,db)