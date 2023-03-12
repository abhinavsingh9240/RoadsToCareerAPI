from sqlalchemy.orm import Session, joinedload
import models
import schemas
from typing import Union

class EducationOps:

    """
        This class include CRUD operations of "education" table
    """

    # CREATE

    def add(education:str,db:Session):

        instance = models.Education(name = education)

        db.add(instance)
        db.commit()
        db.refresh(instance)

        return instance
    
    # READ

    def get(id:int,db:Session):
        return db.query(models.Education).filter(models.Education.id == id).one_or_none()
    
    def get_all(id:int, db:Session):
        return db.query(models.Education).all()
    
    # DELETE

    def delete(id:int,db:Session):
        db.query(models.Education).filter(models.Education.id == id).delete(synchronize_session=False)
        db.commit()
        return True
    
    # UPDATE

    def update(id:int,education:str,db:Session):
        db.query(models.Education).filter(models.Education.id == id).update({models.Education.name: education},synchronize_session=False)
        db.commit()
        return True