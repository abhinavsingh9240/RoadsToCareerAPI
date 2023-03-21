from sqlalchemy.orm import Session, joinedload
import models
class ContributorOps:

    def get_contributor_profile(id:int,db:Session):
        response = db.query(models.User).\
            filter(models.User.id == id).\
            options(joinedload(models.User.contributor)).one_or_none()
        return response
    
    def get_contributor_courses(id:int,db:Session):
        response = db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            options(joinedload(models.Contributor.created_courses)).one_or_none()
        
        return response.created_courses
    
    def get_contributor_roles(id:int,db:Session):
        response = db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            options(joinedload(models.Contributor.created_roles)).one_or_none()
        
        return response.created_roles
    
    def get_contributor_skills(id:int,db:Session):
        response = db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            options(joinedload(models.Contributor.created_skills)).one_or_none()
        
        return response.created_skills
    
    def update_description(newdesc:str,id:int,db:Session):
        db.query(models.Contributor).\
            filter(models.Contributor.id == id).\
            update({models.Contributor.description:newdesc},synchronize_session=False)
        db.commit()
        return ContributorOps.get_contributor_profile(id,db)
    