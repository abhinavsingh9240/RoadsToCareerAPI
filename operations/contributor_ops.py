from sqlalchemy.orm import Session, joinedload
import models
from operations.user_ops import UserOps
from typing import Union
from fastapi import HTTPException,status
class ContributorOps:

    def promote(user_id:int,db:Session):
        contributor = models.Contributor(id = user_id,description = "")
        db.add(contributor)
        db.commit()
        return contributor
    
    def demote(user_id:int,db:Session):
        db.query(models.Contributor).filter(models.Contributor.id == user_id).delete(synchronize_session=False)
        db.commit()
        return True

    def get_contributor_profile(db:Session,email:Union[str,None]= None,id:Union[int,None] = None):
        if id is None:
            id = UserOps.get_id_by_email(email,db)
        response = db.query(models.User).\
            filter(models.User.id == id).\
            options(joinedload(models.User.contributor)).one_or_none()
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User Not Found")
        return response
    

    def get_contributor_courses(db:Session,email:Union[str,None]= None,id:Union[int,None] = None):
        if id is None:
            id = UserOps.get_id_by_email(email,db)
        response = db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            options(joinedload(models.Contributor.created_courses)).one_or_none()
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User Not Found")
        return response.created_courses
    

    def get_contributor_roles(db:Session,email:Union[str,None]= None,id:Union[int,None] = None):
        if id is None:
            id = UserOps.get_id_by_email(email,db)
        response = db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            options(joinedload(models.Contributor.created_roles)).one_or_none()
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User Not Found")
        return response.created_roles
    

    def get_contributor_skills(db:Session,email:Union[str,None]= None,id:Union[int,None] = None):
        if id is None:
            id = UserOps.get_id_by_email(email,db)
        response = db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            options(joinedload(models.Contributor.created_skills)).one_or_none()
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User Not Found")
        return response.created_skills
    
    def update_description(newdesc:str,email:str,db:Session):
        id = UserOps.get_id_by_email(email,db)
        db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            update({models.Contributor.description:newdesc},synchronize_session=False)
        db.commit()
        return ContributorOps.get_contributor_profile(db = db,id=id)
    