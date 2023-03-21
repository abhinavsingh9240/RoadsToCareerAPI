from sqlalchemy.orm import Session, joinedload
import models, schemas
from operations.user_ops import UserOps
from fastapi import HTTPException,status

class SkillOps:

    def add_skill(db: Session, skill: schemas.Skill,email:str):
        id = UserOps.get_id_by_email(email=email,db=db)
        creator = db.query(models.Contributor).filter(models.Contributor.id == id).one_or_none()
        if creator is None:
             raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not Authorized to create skill")

        skill_instance = models.Skill(name=skill.name, description = skill.description, creator_id = id)

        for x in skill.roles_for_skill:
            roles = db.query(models.Role).filter(models.Role.id == x).first()
            skill_instance.roles_for_skill.append(roles)

        for x in skill.courses_for_skill:
            course = db.query(models.Course).filter(models.Course.id == x).first()
            skill_instance.courses_for_skill.append(course)
        
        db.add(skill_instance)
        db.commit()
        db.refresh(skill_instance)
        return SkillOps.show_skill_id(skill_instance.id, db=db)

    
    def show_skill_all(db: Session):
        return db.query(models.Skill).options(joinedload(models.Skill.roles_for_skill), joinedload(models.Skill.courses_for_skill)).all()

    def show_skill_id(id: int, db: Session):
        result = db.query(models.Skill).filter(models.Skill.id == id)
        result = result.options(joinedload(models.Skill.roles_for_skill), joinedload(models.Skill.courses_for_skill))
        
        return result.first()

    def skill_search(search_query: str, db: Session):
        whole_result = set()
        # first we will search for the skill starting with entered query
        partial_result = db.query(models.Skill).filter(
            models.Skill.name.ilike(f"{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        # then we will search for the skill having entered query as substring
        partial_result = db.query(models.Skill).filter(
            models.Skill.name.ilike(f"%{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        return whole_result
    
    def update(skill_id:int,skill:schemas.Skill,db:Session,email:str):

        user_id = UserOps.get_id_by_email(email=email,db = db)
        skill_instance = db.query(models.Skill).filter(models.Skill.id == skill_id).one_or_none()
        if skill_instance.creator_id != user_id :
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not Authorized for this skill")
        
        skill_instance.name = skill.name
        skill_instance.description = skill.description
        
        skill_instance.courses_for_skill.clear()
        skill_instance.roles_for_skill.clear()

        for x in skill.roles_for_skill:
            roles = db.query(models.Role).filter(models.Role.id == x).first()
            skill_instance.target.append(roles)
        for x in skill.courses_for_skill:
            course = db.query(models.Course).filter(models.Course.id == x).first()
            skill_instance.courses_for_skill.append(course)

        db.commit()

        return True

    def remove(skill_id:int,db:Session,email:str):

        user_id = UserOps.get_id_by_email(email=email,db = db)
        skill_instance = db.query(models.Skill).filter(models.Skill.id == skill_id).one_or_none()
        if skill_instance.creator_id != user_id :
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not Authorized for this skill")
        
        skill_instance.courses_for_skill.clear()
        skill_instance.roles_for_skill.clear()

        db.query(models.Skill).filter(models.Skill.id == skill_id).delete(synchronize_session=False)
        db.commit()
        return True
        

