from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from operations.course_ops import CourseOps

router = APIRouter(
    prefix="/course",
    tags=["Courses"],
)

"""
    MAP FOR COURSES 
    GET     /course/                            -> return all courses
    POST    /course/                            -> Create New Course
    GET     /course/{id}                        -> return course with {id}
    PUT     /course/{id}                        -> update the whole course of {id}
    GET     /course/search                      -> search course with given string
    DELETE  /course/{id}                        -> delete the course with given id 
    PUT     /course/{id}/name                   -> update the course name
    DELETE  /course/{id}/skill/{skill_id}       -> delete the skill of skill_id for that course
    DELETE  /course/{id}/career/{career_id}     -> delete the career of career_id for that course
    POST    /course/{id}/skill/{skill_id}       -> add the skill of skill_id in that course
    POST    /course/{id}/career/{career_id}     -> add the coure of course_id in that course

    to be added in future:
    PUT     /course/{id}/price                  -> update the course price
    PUT     /course/{id}/link                   -> update the course link
        
        .....
"""

@router.post("/")
def post_course(course:schemas.Course,db:Session = Depends(get_db)):
    return CourseOps.add_course(course=course,db=db)

@router.get("/")
def get_course(db:Session = Depends(get_db)):
    return CourseOps.show_course_all(db=db)

@router.get("/{id}")
def get_course_by_id(id:int,db:Session = Depends(get_db)):
    return CourseOps.show_course_id(id,db)

@router.get("/search/{query}")
def get_course_by_name(query:str,db:Session = Depends(get_db)):
    return CourseOps.course_search(query,db)

@router.delete("/{id}")
def delete_course(id:int,db:Session = Depends(get_db)):
    return {"Done"} if CourseOps.remove_course(id=id,db=db) else {"Not Completed"}

@router.put("/{id}")
def update_course(id,request:schemas.Course,db:Session = Depends(get_db)):
    CourseOps.update_course(id,request,db)
    return {"Done"}