from sqlalchemy.orm import Session, joinedload
import models
import schemas


class CourseOps:

    def add_course(db: Session, course: schemas.Course):
        course_instance = models.Course(name=course.name)
        for x in course.career:
            career = db.query(models.Career).filter(
                models.Career.id == x).first()
            course_instance.target_career.append(career)

        for x in course.skill:
            skill = db.query(models.Skill).filter(models.Skill.id == x).first()
            course_instance.target_skill.append(skill)

        db.add(course_instance)
        db.commit()
        db.refresh(course_instance)

        return CourseOps.show_course_id(course_instance.id, db=db)


    def show_course_all(db: Session):
        return db.query(models.Course).options(joinedload(models.Course.target_career), joinedload(models.Course.target_skill)).all()


    def show_course_id(id: int, db: Session):
        result = db.query(models.Course).filter(models.Course.id == id)
        result = result.options(joinedload(
            models.Course.target_career), joinedload(models.Course.target_skill))
        return result.first()


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
        course_instance.target_career.clear()
        db.query(models.Course).filter(models.Course.id == id).delete(synchronize_session=False)
        db.commit()
        return True
    
    def update_course(id:int,course:schemas.Course, db:Session):
        # db.query(models.Course).filter(models.Course.id == id).update({models.Course.name : course.name},synchronize_session=False)
        
        course_instance = db.query(models.Course).filter(models.Course.id == id).one_or_none()
        course_instance.target_skill.clear()
        course_instance.target_career.clear()
        for x in course.career:
            career = db.query(models.Career).filter(
                models.Career.id == x).first()
            course_instance.target_career.append(career)

        for x in course.skill:
            skill = db.query(models.Skill).filter(models.Skill.id == x).first()
            course_instance.target_skill.append(skill)

        db.commit()
        return True