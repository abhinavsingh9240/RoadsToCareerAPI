from sqlalchemy.orm import Session, joinedload
import models
import schemas
from typing import Union


class LanguageOps:

    """
        This class include CRUD operations of "languages" table
    """

    # CREATE

    def add(language_name:str,db:Session):

        instance = models.Language(name = language_name)

        db.add(instance)
        db.commit()
        db.refresh(instance)

        return instance
    
    # READ

    def get(id:int,db:Session):
        return db.query(models.Language).filter(models.Language.id == id).one_or_none()

    def get_all(db:Session):
        return db.query(models.Language).all()

    # DELETE

    def delete(id:int,db:Session):
        
        db.query(models.Language).filter(models.Language.id == id).delete(synchronize_session=False)
        db.commit()

        return True
    
    # UPDATE
    def update(id:int,new_name:str,db:Session):

        db.query(models.Language).\
            filter(models.Language.id == id).\
                update({models.Language.name:new_name},synchronize_session=False)
        
        db.commit()

        return True
    
    