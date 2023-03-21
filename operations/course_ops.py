from fastapi import HTTPException,status
from sqlalchemy.orm import Session, joinedload
import models
import schemas


class CourseOps:

    def add_course(db: Session, course: schemas.CourseBase,user_id:int):
        contrib_instance = db.query(models.Contributor).filter(models.Contributor.id == id).one_or_none()
        if contrib_instance is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Not Authorized to Create course,Need to be a contributor")
        
        course_instance = models.Course(name=course.name,
                                        link = course.link,
                                        duration_hours = course.duration_hours,
                                        is_free = course.is_free,
                                        )
        course_instance.creator = contrib_instance
             
        for x in course.roles:
            role = db.query(models.Role).filter(
                models.Role.id == x).one_or_none()
            course_instance.target_roles.append(role)

        for x in course.target_skills:
            skill = db.query(models.Skill).filter(models.Skill.id == x).one_or_none()
            course_instance.target_skill.append(skill)

        for x in course.skills_required:
            skill = db.query(models.Skill).filter(models.Skill.id == x).one_or_none()
            course_instance.skills_required.append(skill)
        
        for x in course.languages:
            language = db.query(models.Language).filter(models.Skill.id == x).one_or_none()
            course_instance.language.append(language)


        db.add(course_instance)
        db.commit()
        db.refresh(course_instance)

        return CourseOps.show_course_id(course_instance.id, db=db)


    def show_course_all(db: Session):
        return db.query(models.Course).all()
    
    
    def show_course_id(id: int, db: Session):
        response = db.query(models.Course).filter(models.Course.id == id)
        response = response.options(joinedload(models.Course.target_roles), 
                    joinedload(models.Course.target_skill),
                    joinedload(models.Course.skills_required),
                    joinedload(models.Course.language),
                    )
        return response.one_or_none()

    def course_search(search_query: str, db: Session):
        whole_result = set()
        # first we will search for the Course starting with entered query
        partial_result = db.query(models.Course).filter(
            models.Course.name.ilike(f"{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        # then we will search for the Course having entered query as substring
        partial_result = db.query(models.Course).filter(
            models.Course.name.ilike(f"%{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        return whole_result


    def remove_course(id: int, db:Session):
        course_instance = db.query(models.Course).filter(models.Course.id == id).one_or_none()
        course_instance.target_skill.clear()
        course_instance.target_roles.clear()
        course_instance.liked_by.clear()
        db.query(models.Course).filter(models.Course.id == id).delete(synchronize_session=False)
        db.commit()
        return True
    
    def update_course(id:int,course:schemas.CourseBase, db:Session):
        course_instance = db.query(models.Course).filter(models.Course.id == id).\
            update({"name":course.name,
                    "link" : course.link,
                    "duration_hours" : course.duration_hours,
                    "is_free" : course.is_free,},synchronize_session=False)
        course_instance = db.query(models.Course).filter(models.Course.id == id).one_or_none()
        course_instance.target_skill.clear()
        course_instance.target_roles.clear()
        course_instance.liked_by.clear()
        
        for x in course.roles:
            role = db.query(models.Role).filter(
                models.Role.id == x).one_or_none()
            course_instance.target_roles.append(role)

        for x in course.target_skills:
            skill = db.query(models.Skill).filter(models.Skill.id == x).one_or_none()
            course_instance.target_skill.append(skill)

        for x in course.skills_required:
            skill = db.query(models.Skill).filter(models.Skill.id == x).one_or_none()
            course_instance.skills_required.append(skill)
        
        for x in course.languages:
            language = db.query(models.Language).filter(models.Skill.id == x).one_or_none()
            course_instance.language.append(language)
        
        db.commit()
        db.refresh(course_instance)
        return CourseOps.show_course_id(course_instance.id, db=db)