from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
from operations.roletype_ops import RoleTypeOps

router = APIRouter(
    prefix="/roletype",
    tags=["Role Type"]
)

@router.post("",status_code=status.HTTP_201_CREATED)
def add_roletype(title:str,db:Session = Depends(get_db)):
    return RoleTypeOps.add(name= title,db = db)

@router.get("",status_code=status.HTTP_202_ACCEPTED)
def get_roletype(db:Session = Depends(get_db)):
    return RoleTypeOps.get_all(db=db)

@router.get("/{id}",status_code=status.HTTP_202_ACCEPTED)
def get_roletype_by_id(id:int,db:Session = Depends(get_db)):
    response =  RoleTypeOps.get(id,db)
    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"roletype of id: {id} is not available")
    return response

@router.delete("/{id}",status_code=status.HTTP_202_ACCEPTED)
def remove_roletype(id:int,db:Session = Depends(get_db)):
    response = RoleTypeOps.delete(id,db)
    return response

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_roletype(id:int,new_name:str,db:Session = Depends(get_db)):
    return RoleTypeOps.update(id,type = new_name,db=db)

@router.put("/search/{query}")
def search_roletype(query:str,db:Session = Depends(get_db)):
    return RoleTypeOps.search(query,db)