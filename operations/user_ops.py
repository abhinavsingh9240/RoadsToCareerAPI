from fastapi import HTTPException,status
from sqlalchemy.orm import Session, joinedload
from hashing import Hash
import models
import schemas

class UserOps:
    
    def get_by_id(id:int,db:Session):
        user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
        if not user_instance.contributor is None:
            user_instance["is_contributor"] = True
        else:
            user_instance["is_contributor"] = False
        
        return user_instance
    
    def liked_courses(id:int,db:Session):

        user_instance = db.query(models.User).\
            filter(models.User.id == id).options(joinedload(models.User.liked_courses)).\
            one_or_none()
        
        return user_instance.liked_courses
    
    def liked_roles(id:int,db:Session):
        
        user_instance = db.query(models.User).\
            filter(models.User.id == id).\
                options(joinedload(models.User.liked_roles)).\
            one_or_none()
        
        return user_instance.liked_roles

    def liked_skills(id:int,db:Session):
        
        user_instance = db.query(models.User).\
            filter(models.User.id == id).\
                options(joinedload(models.User.liked_skills)).\
            one_or_none()
        
        return user_instance.liked_skills
    
    def update_name(request:schemas.NameUpdate,id:int,db:Session):
        user = db.query(models.User).filter(models.User.id == id).one_or_none()
        
        if not Hash.verify_password(request.password,user.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")
            
        db.query(models.User).filter(models.User.id == id).\
            update({models.User.email:request.name},synchronize_session=False)

        db.commit()
        return UserOps.get_by_id(id,db)
    
    def update_email(request:schemas.EmailUpdate,id:int,db:Session):
        user = db.query(models.User).filter(models.User.id == id).one_or_none()
        
        if not Hash.verify_password(request.password,user.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")
            
        db.query(models.User).filter(models.User.id == id).\
            update({models.User.email:request.email},synchronize_session=False)

        db.commit()
        return UserOps.get_by_id(id,db)
        
    def update_password(request:schemas.PasswordUpdate,id:int,db:Session):

        user = db.query(models.User).filter(models.User.id == id).one_or_none()

        if not Hash.verify_password(request.password,user.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")
        
        new_hashed_password = Hash.get_password_hash(request.new_password)
        db.query(models.User).filter(models.User.id == id).\
            update({models.User.password : new_hashed_password},synchronize_session=False)
        db.commit()
        return True

        

