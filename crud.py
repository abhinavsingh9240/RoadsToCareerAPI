from sqlalchemy.orm import Session, joinedload
import schemas
import models


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

    return show_career_id(career_instance.id, db=db)


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
    return show_skill_id(skill_instance.id, db=db)


def add_course(db: Session, course: schemas.course):
    course_instance = models.Course(name=course.name)
    for x in course.career:
        career = db.query(models.Career).filter(models.Career.id == x).first()
        course_instance.target_career.append(career)

    for x in course.skill:
        skill = db.query(models.Skill).filter(models.Skill.id == x).first()
        course_instance.target_skill.append(skill)

    db.add(course_instance)
    db.commit()
    db.refresh(course_instance)

    return show_course_id(course_instance.id,db = db)


def show_career_all(db: Session):

    return db.query(models.Career).options(joinedload(models.Career.requirements), joinedload(models.Career.courses_for_career)).all()


def show_skill_all(db: Session):

    return db.query(models.Skill).options(joinedload(models.Skill.target), joinedload(models.Skill.courses_for_skill)).all()


def show_course_all(db: Session):
    return db.query(models.Course).options(joinedload(models.Course.target_career), joinedload(models.Course.target_skill)).all()


def show_career_id(id: int, db: Session):
    result = db.query(models.Career).filter(models.Career.id == id)
    result = result.options(joinedload(models.Career.requirements), joinedload(models.Career.courses_for_career))
    return result.first()


def show_skill_id(id: int, db: Session):
    result = db.query(models.Skill).filter(models.Skill.id == id)
    result = result.options(joinedload(models.Skill.target), joinedload(models.Skill.courses_for_skill))
    return result.first()

def show_course_id(id:int, db: Session):
    result = db.query(models.Course).filter(models.Course.id == id)
    result = result.options(joinedload(models.Course.target_career), joinedload(models.Course.target_skill))
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

    # Not tested -->
    # new_search_query = '%'.join(i for i in search_query)
    # partial_result = db.query(models.Skill).filter(models.Skill.name.ilike(f"{search_query}")).all()
    # whole_result =whole_result.union(set(partial_result))

    # partial_result = db.query(models.Skill).filter(models.Skill.name.ilike(f"{search_query}%")).all()
    # whole_result =whole_result.union(set(partial_result))

    # partial_result = db.query(models.Skill).filter(models.Skill.name.ilike(f"%{search_query}%")).all()
    # whole_result =whole_result.union(set(partial_result))

    return whole_result


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

    # Not tested -->
    # new_search_query = '%'.join(i for i in search_query)
    # partial_result = db.query(models.Career).filter(models.Career.name.ilike(f"{search_query}")).all()
    # whole_result =whole_result.union(set(partial_result))

    # partial_result = db.query(models.Career).filter(models.Career.name.ilike(f"{search_query}%")).all()
    # whole_result =whole_result.union(set(partial_result))

    # partial_result = db.query(models.Career).filter(models.Career.name.ilike(f"%{search_query}%")).all()
    # whole_result =whole_result.union(set(partial_result))

    return whole_result

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

    # Not tested -->
    # new_search_query = '%'.join(i for i in search_query)
    # partial_result = db.query(models.Course).filter(models.Course.name.ilike(f"{search_query}")).all()
    # whole_result =whole_result.union(set(partial_result))

    # partial_result = db.query(models.Course).filter(models.Course.name.ilike(f"{search_query}%")).all()
    # whole_result =whole_result.union(set(partial_result))

    # partial_result = db.query(models.Course).filter(models.Course.name.ilike(f"%{search_query}%")).all()
    # whole_result =whole_result.union(set(partial_result))

    return whole_result
