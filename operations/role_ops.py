from sqlalchemy.orm import Session, joinedload
import models
from operations.user_ops import UserOps
import schemas
from fastapi import HTTPException,status


class RoleOps:

    def show_role_all(db: Session):
        return db.query(models.Role).all()

    def show_role_id(id: int, db: Session):
        response = db.query(models.Role).filter(models.Role.id == id)
        response = response.options(
            joinedload(models.Role.required_skills),
            joinedload(models.Role.courses_for_role),
            joinedload(models.Role.education))
        return response.first()

    def career_search(search_query: str, db: Session):
        whole_result = set()
        # first we will search for the Career starting with entered query
        partial_result = db.query(models.Role).filter(
            models.Role.name.ilike(f"{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        # then we will search for the Career having entered query as substring
        partial_result = db.query(models.Role).filter(
            models.Role.name.ilike(f"%{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        return whole_result

    def add(db: Session, career: schemas.RoleBase,email:str):
        user_id = UserOps.get_id_by_email(email,db)
        contributor_instance = db.query(models.Contributor).filter(models.Contributor.id == user_id).one_or_none()
        if contributor_instance is None:
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not A Contributor") 
        
        role_instance = models.Role(name=career.name, 
                                        description = career.description,
                                        avg_salary = career.avg_salary,
                                        type_id = career.type_id,
                                        creator_id = user_id
                                        )
        
        for x in career.required_skills:
            skill = db.query(models.Skill).filter(models.Skill.id == x).first()
            role_instance.required_skills.append(skill)

        for x in career.courses_for_role:
            course = db.query(models.Course).filter(
                models.Course.id == x).first()
            role_instance.courses_for_role.append(course)
        
        for x in career.education:
            edu = db.query(models.Education).filter(
                models.Education.id == x
            ).first()
            role_instance.education.append(edu)
        
        
        db.add(role_instance)
        db.commit()
        db.refresh(role_instance)

        return RoleOps.show_role_id(role_instance.id, db=db)

    def update(id: int, career: schemas.RoleBase, db: Session,email:str):
        user_id = UserOps.get_id_by_email(email,db)
        role_instance = db.query(models.Role).filter(
            models.Role.id == id).one_or_none()
        if role_instance.creator_id != user_id:
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                                detail="You are not the creator of course")

        role_instance.name = career.name
        role_instance.avg_salary = career.avg_salary
        role_instance.description = career.description
        role_instance.type_id = career.type_id

        role_instance.required_skills.clear()
        role_instance.courses_for_role.clear()
        role_instance.education.clear()

        for x in career.required_skills:
            skill = db.query(models.Skill).filter(models.Skill.id == x).first()
            role_instance.required_skills.append(skill)
        for x in career.courses_for_role:
            course = db.query(models.Course).filter(
                models.Course.id == x).first()
            role_instance.courses_for_role.append(course)
        for x in career.education:
            edu = db.query(models.Education).filter(models.Education.id==x).first()
            role_instance.education.append(edu)

        db.commit()
        return True

    def remove(id: int, db: Session,email:str):
        user_id = UserOps.get_id_by_email(email,db)
        role_instance = db.query(models.Role).filter(
            models.Role.id == id).one_or_none()
        if role_instance.creator_id != user_id:
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                                detail="You are not the creator of course")

        role_instance.required_skills.clear()
        role_instance.courses_for_role.clear()
        role_instance.education.clear()



        db.query(models.Career).filter(models.Career.id == id).delete(synchronize_session=False)
        db.commit()
        return True
