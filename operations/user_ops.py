from fastapi import HTTPException,status
from sqlalchemy.orm import Session, joinedload
from hashing import Hash
import models
import schemas

class UserOps:
    
    def get_id_by_email(email:str,db:Session):
        user =  db.query(models.User).filter(models.User.email == email).one_or_none()
        return user.id
    def get_by_id(id:int,db:Session):
        user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
        
        return user_instance
    
    def get_user(email:str,db:Session):
        user_instance = db.query(models.User).filter(models.User.email == email).one_or_none()
        
        return user_instance

    
    def liked_courses(email:str,db:Session):


        user_instance = db.query(models.User).\
            filter(models.User.email == email).options(joinedload(models.User.liked_courses)).\
            one_or_none()
        
        return user_instance.liked_courses
    
    def liked_roles(email:str,db:Session):
        
        user_instance = db.query(models.User).\
            filter(models.User.email == email).\
                options(joinedload(models.User.liked_roles)).\
            one_or_none()
        
        return user_instance.liked_roles

    def liked_skills(email:str,db:Session):
        
        user_instance = db.query(models.User).\
            filter(models.User.email == email).\
                options(joinedload(models.User.liked_skills)).\
            one_or_none()
        
        return user_instance.liked_skills
    
    def update_name(request:schemas.NameUpdate,email:str,db:Session):
        user = db.query(models.User).filter(models.User.email == email).one_or_none()
        
        if not Hash.verify_password(request.password,user.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")
            
        db.query(models.User).filter(models.User.email == email).\
            update({models.User.name:request.name},synchronize_session=False)

        db.commit()
        return UserOps.get_by_id(email,db)
    
    def update_email(request:schemas.EmailUpdate,email:str,db:Session):
        user = db.query(models.User).filter(models.User.email == email).one_or_none()
        
        if not Hash.verify_password(request.password,user.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")
            
        db.query(models.User).filter(models.User.email == email).\
            update({models.User.email:request.email},synchronize_session=False)

        db.commit()
        return UserOps.get_by_id(email,db)
        
    def update_password(request:schemas.PasswordUpdate,email:str,db:Session):

        user = db.query(models.User).filter(models.User.email == email).one_or_none()

        if not Hash.verify_password(request.password,user.password):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Invalid Password/Username")
        
        new_hashed_password = Hash.get_password_hash(request.new_password)
        db.query(models.User).filter(models.User.email == email).\
            update({models.User.password : new_hashed_password},synchronize_session=False)
        db.commit()
        return True

        

