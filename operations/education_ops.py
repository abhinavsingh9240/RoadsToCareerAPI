from sqlalchemy.orm import Session, joinedload
import models
import schemas
from typing import Union

class EducationOps:

    """
        This class include CRUD operations of "education" table
    """

    # CREATE

    def add(request:schemas.EducationBase,db:Session):

        instance = models.Education(name = request.name,duration_year = request.duration_year)

        db.add(instance)
        db.commit()
        db.refresh(instance)

        return instance
    
    # READ

    def get(id:int,db:Session):
        return db.query(models.Education).filter(models.Education.id == id).one_or_none()
    
    def get_all( db:Session):
        return db.query(models.Education).all()
    
    # DELETE

    def delete(id:int,db:Session):
        education_instance = db.query(models.Education).filter(models.Education.id == id).one_or_none()
        education_instance.roles.clear()
        db.query(models.Education).filter(models.Education.id == id).delete(synchronize_session=False)
        db.commit()
        return True
    
    # UPDATE

    def update(id:int,education:schemas.EducationBase,db:Session):
        db.query(models.Education).filter(models.Education.id == id).update({models.Education.name: education.name,models.Education.duration_year:education.duration_year},synchronize_session=False)
        db.commit()
        return EducationOps.get(id,db)
    
    def search(search_query:str,db:Session):
        result = set()
        partial_result = db.query(models.Education).\
            filter(models.Education.name.ilike(f"{search_query}%")).all()

        result = result.union(set(partial_result))

        partial_result = db.query(models.Education).\
            filter(models.Education.name.ilike(f"%{search_query}%")).all()
        
        result = result.union(set(partial_result))

        return result
    