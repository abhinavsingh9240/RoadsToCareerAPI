from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from oauth2 import OAuth2
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
        .....
"""

@router.post("/")
def post_course(course:schemas.CourseBase,db:Session = Depends(get_db),user_id:int = Depends(OAuth2.get_current_user)):
    return CourseOps.add_course(course=course,db=db,user_id = user_id)

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