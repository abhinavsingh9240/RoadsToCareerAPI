from sqlalchemy.orm import Session, joinedload
import models, schemas

class SkillOps:

    def add_skill(db: Session, skill: schemas.skill):
        skill_instance = models.Skill(name=skill.name)
        for x in skill.career:
            career = db.query(models.Career).filter(models.Career.id == x).first()
            skill_instance.target.append(career)
        for x in skill.course:
            course = db.query(models.Course).filter(models.Course.id == x).first()
            skill_instance.courses_for_skill.append(course)
        db.add(skill_instance)
        db.commit()
        db.refresh(skill_instance)
        return SkillOps.show_skill_id(skill_instance.id, db=db)

    
    def show_skill_all(db: Session):
        return db.query(models.Skill).options(joinedload(models.Skill.target), joinedload(models.Skill.courses_for_skill)).all()

    def show_skill_id(id: int, db: Session):
        result = db.query(models.Skill).filter(models.Skill.id == id)
        result = result.options(joinedload(models.Skill.target), joinedload(models.Skill.courses_for_skill))
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
