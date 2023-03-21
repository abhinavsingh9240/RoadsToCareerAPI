from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
from operations.language_ops import LanguageOps

router = APIRouter(
    tags=["Language"],
    prefix= "/language"
)

@router.post("",status_code=status.HTTP_201_CREATED)
def add_language(name:str,db:Session = Depends(get_db)):
    return LanguageOps.add(language_name=name, db=db)

@router.get("",status_code=status.HTTP_202_ACCEPTED)
def get_language(db:Session = Depends(get_db)):
    response =  LanguageOps.get_all(db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language Not Found")
    
    return response

@router.get("/{id}",status_code=status.HTTP_202_ACCEPTED)
def get_language_by_id(id:int,db:Session = Depends(get_db)):
    response = LanguageOps.get(id,db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language Not Found")
    
    return response

@router.delete("/{id}",status_code=status.HTTP_202_ACCEPTED)
def remove_language(id:int,db:Session = Depends(get_db)):
    response = LanguageOps.delete(id,db)
    if response is True:
        return {"Detail": "Deleted Sucessfully"}
    else:
        return {"Detail": "Some Error Occured"}
    
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_language(id:int,name:str,db:Session = Depends(get_db)):
    response = LanguageOps.update(id,name,db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language Not Found")
    return response

@router.get("/search/{query}")
def search_language(query:str,db:Session = Depends(get_db)):
    response =  LanguageOps.search(query,db)
    if response is None or not response :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language Not Found")
    return response