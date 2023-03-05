from fastapi import FastAPI, Depends
from database import engine

import models 
from routers import authenticate, career ,skill, course

#body
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authenticate.router)
app.include_router(career.router)
app.include_router(skill.router)
app.include_router(course.router)


@app.get("/")
def home():
    return {"message":"Welcome to Career Map API"}

