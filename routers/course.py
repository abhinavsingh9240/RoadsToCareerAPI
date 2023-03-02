from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from operations.course_ops import CourseOps

router = APIRouter(
    prefix="/course",
    tags=["Courses"],
)

@router.post("/")
def post_course(course:schemas.course,db:Session = Depends(get_db)):
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