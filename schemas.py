from pydantic import BaseModel
from typing import List,Union

class Career(BaseModel):
    name:str
    skill:List[int] = [] 
    course:List[int] = []

class Skill(BaseModel):
    name:str
    career:List[int] = []
    course:List[int] = []

class Course(BaseModel):
    name:str
    skill:List[int] = []
    career:List[int] = []

class User(BaseModel):
    name:str
    email:str
    password:str

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
