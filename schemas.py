from pydantic import BaseModel
from typing import List,Union,Dict

class Base(BaseModel):
    id:int
    name:str
    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name:str
    description:str
    avg_salary: int
    type_id:int
    required_skills : List[int] = []
    courses_for_role: List[int] = []
    education:List[int] = []

class Skill(BaseModel):
    name:str
    description:str
    roles_for_skill:List[int] = []
    courses_for_skill:List[int] = []


class CourseBase(BaseModel):
    name:str
    link:str
    duration_hours:int
    is_free:bool
    roles:List[int] = []
    target_skills:List[int] = []
    languages:List[int] = []
    skills_required:List[int] = []
    

class UserBase(BaseModel):
    name:str
    email:str
    class Config:
        orm_mode = True

class Register(BaseModel):
    name:str
    email:str
    password:str

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class NameUpdate(BaseModel):
    name:str
    password:str

class EmailUpdate(BaseModel):
    email:str
    password:str

class PasswordUpdate(BaseModel):
    old_password:str
    new_password:str

class UpdateContribDesc(BaseModel):
    desc:str

class EducationBase(BaseModel):
    name:str
    duration_year:int

class ContributorBase(BaseModel):
    description:str
    class Config:
        orm_mode = True


class ContributorResponse(BaseModel):
    name:str
    email:str   
    contributor: ContributorBase

    class Config:
        orm_mode = True

    