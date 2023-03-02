from sqlalchemy.orm import Session, joinedload
import models, schemas

class CareerOps:

    def show_career_all(db: Session):

        return db.query(models.Career).options(joinedload(models.Career.requirements), joinedload(models.Career.courses_for_career)).all()
    
    def show_career_id(id: int, db: Session):
        result = db.query(models.Career).filter(models.Career.id == id)
        result = result.options(joinedload(models.Career.requirements), joinedload(models.Career.courses_for_career))
        return result.first()

    def career_search(search_query: str, db: Session):
        whole_result = set()
        # first we will search for the Career starting with entered query
        partial_result = db.query(models.Career).filter(
            models.Career.name.ilike(f"{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        # then we will search for the Career having entered query as substring
        partial_result = db.query(models.Career).filter(
            models.Career.name.ilike(f"%{search_query}%")).all()
        whole_result = whole_result.union(set(partial_result))

        return whole_result
    
    def add_career(db: Session, career: schemas.career):
        career_instance = models.Career(name=career.name)
        for x in career.skill:
            skill = db.query(models.Skill).filter(models.Skill.id == x).first()
            career_instance.requirements.append(skill)
        for x in career.course:
            course = db.query(models.Course).filter(models.Course.id == x).first()
            career_instance.courses_for_career.append(course)
        db.add(career_instance)
        db.commit()
        db.refresh(career_instance)

        return CareerOps.show_career_id(career_instance.id, db=db)
    