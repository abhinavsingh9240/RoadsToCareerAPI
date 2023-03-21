from pydantic import BaseModel
from typing import List,Union

class Base(BaseModel):
    id:int
    name:str

class CourseBase(BaseModel):
    name:str
    link:str
    duration_hours:int
    is_free:bool
    roles:List[int]
    target_skills:List[int]
    languages:List[int]
    skills_required:List[int]
    

class UserBase(BaseModel):
    name:str
    email:str
    is_contributor:bool

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