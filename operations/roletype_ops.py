from sqlalchemy.orm import Session, joinedload
import models
import schemas

class RoleTypeOps:
    """
        This Class includes all CRUD operations related to "roletypes" table
    """

    # CREATE
    def add(name:str,db:Session):

        instance = models.RoleType(name = name)

        db.add(instance)
        db.commit()
        db.refresh(instance)

        return instance
    
    # READ
    def get(id:int,db:Session):

        return db.query(models.RoleType).filter(models.RoleType.id == id).one_or_none()
    
    def get_all(db:Session):

        return db.query(models.RoleType).all()
    
    # DELETE
    def delete(id:int,db:Session):

        db.query(models.RoleType).filter(models.RoleType.id == id).delete(synchronize_session=False)
        db.commit()
        return True

    # UPDATE
    def update(id:int,type:str,db:Session):
        
        db.query(models.RoleType).filter(models.RoleType.id == id).update({models.RoleType.name: type},synchronize_session=False)
        db.commit()
        return True
    
    def search(search_query:str,db:Session):

        result = set()
        partial_result = db.query(models.RoleType).filter(models.RoleType.name.ilike(f"{search_query}%"))

        result = result.union(set(partial_result))

        partial_result = db.query(models.RoleType).filter(models.RoleType.name.ilike(f"%{search_query}%"))

        result = result.union(set(partial_result))

        return result

        
    


