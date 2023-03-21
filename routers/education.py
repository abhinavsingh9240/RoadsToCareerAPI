from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
from operations.education_ops import EducationOps

router = APIRouter(
    prefix="/education",
    tags = ["Education"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_education(request:schemas.EducationBase,db:Session = Depends(get_db)):
    return EducationOps.add(request,db)

@router.get("/",status_code=status.HTTP_202_ACCEPTED)
def get_educations(db:Session = Depends(get_db)):
    response = EducationOps.get_all(db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Educations Not Found")
    return response

@router.get("/{id}",status_code=status.HTTP_202_ACCEPTED)
def get_education_by_id(id:int,db:Session = Depends(get_db)):
    response = EducationOps.get(id,db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Education with {id} not found ")
    
    return response

@router.delete("/{id}")
def remove_education(id:int,db:Session = Depends(get_db)):
    response =  EducationOps.delete(id,db)
    if response is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error Occured")
    
    return response

@router.put("/{id}")
def update_education(id:int,education:schemas.EducationBase,db:Session = Depends(get_db)):
    response = EducationOps.update(id,education,db)

    return response

@router.get("/search/{query}")
def search_education(search_query:str,db:Session = Depends(get_db)):
    response =  EducationOps.search(search_query,db)
    if response is None or not response :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language Not Found")
    return response