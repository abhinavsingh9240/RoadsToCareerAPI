from sqlalchemy.orm import Session, joinedload
import models
import schemas

class UserOps:

    def get_by_email(email:str,db:Session):

        return db.query(models.User).filter(models.User.email == email).one_or_none()
