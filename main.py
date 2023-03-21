from fastapi import FastAPI, Depends
from database import engine

import models ,views
from routers import authenticate, roles ,skill, course, language, education, roletype,contributors,user
from sqladmin import Admin
from admin_auth import AdminAuth
#body
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(authenticate.router)
app.include_router(user.router)
app.include_router(contributors.router)
app.include_router(roles.router)
app.include_router(course.router)
app.include_router(skill.router)
app.include_router(language.router)
app.include_router(education.router)
app.include_router(roletype.router)

admin = Admin(app, engine,authentication_backend=AdminAuth("..."))

admin.add_view(views.User)
admin.add_view(views.Contributor)
admin.add_view(views.Role)
admin.add_view(views.Course)
admin.add_view(views.Skill)
admin.add_view(views.RoleType)
admin.add_view(views.Education)
admin.add_view(views.Language)



@app.get("/")
def home():
    return {"message":"Welcome to Career Map API"}

