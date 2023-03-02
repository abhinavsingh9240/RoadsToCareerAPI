from pydantic import BaseModel
from typing import List,Union

class career(BaseModel):
    name:str
    skill:List[int] = [] 
    course:List[int] = []

class skill(BaseModel):
    name:str
    career:List[int] = []
    course:List[int] = []

class course(BaseModel):
    name:str
    skill:List[int] = []
    career:List[int] = []
