from __future__ import annotations

from sqlalchemy import Column,String
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional

from database import Base



role_skill = Table(
    "role_skill",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
    extend_existing=True,
)

role_course = Table(
    "role_course",
    Base.metadata,
    Column("role_id",ForeignKey("roles.id"),primary_key=True),
    Column("course_id",ForeignKey("courses.id"),primary_key = True),
    extend_existing=True,
)

skill_course = Table(
    "skill_course",
    Base.metadata,
    Column("skill_id",ForeignKey("skills.id"),primary_key=True),
    Column("course_id",ForeignKey("courses.id"),primary_key = True),
    extend_existing=True,
)


courses_liked_by_user = Table(
    "courses_liked_by_user",
    Base.metadata,
    Column("user_id",ForeignKey("users.id"),primary_key=True),
    Column("course_id",ForeignKey("courses.id"),primary_key = True),
    extend_existing=True,
)

roles_liked_by_user = Table(
    "roles_liked_by_user",
    Base.metadata,
    Column("user_id",ForeignKey("users.id"),primary_key=True),
    Column("role_id",ForeignKey("roles.id"),primary_key=True),
    extend_existing=True,
)

skills_liked_by_user = Table(
    "skills_liked_by_user",
    Base.metadata,
    Column("user_id",ForeignKey("users.id"),primary_key=True),
    Column("skill_id",ForeignKey("skills.id"),primary_key=True),
    extend_existing=True,
)

role_education = Table(
    "role_education",
    Base.metadata,
    Column("role_id",ForeignKey("roles.id"),primary_key=True),
    Column("education_id",ForeignKey("education.id"),primary_key=True),
    extend_existing=True,
)


# Classes of Entitiy in Database
# Entities - User, Contributor, Role, Course, Skill, Education, Language, Industry 

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String,unique=True,index=True)
    password: Mapped[str] = mapped_column()
    
    contributor: Mapped[Optional[Contributor]] = relationship(back_populates="user")

    liked_courses: Mapped[List[Course]] = relationship(
        secondary= courses_liked_by_user, back_populates= "liked_by"
    )
    
    liked_roles: Mapped[List[Role]] = relationship(
        secondary=roles_liked_by_user, back_populates= "liked_by"
    )

    liked_skills: Mapped[List[Skill]] = relationship(
        secondary=skills_liked_by_user, back_populates="liked_by"
    )    


class Contributor(Base):
    
    __tablename__ = "contributors"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] =  mapped_column(ForeignKey("users.id"),primary_key=True)
    user: Mapped[User] = relationship(back_populates="contributor")

    description: Mapped[str] = mapped_column()

    created_courses: Mapped[List[Course]] = relationship(back_populates="creator")
    created_roles: Mapped[List[Role]] = relationship(back_populates="creator")
    created_skills: Mapped[List[Skill]] = relationship(back_populates="creator")
    

class Role(Base):

    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String,unique= True)
    descriptions: Mapped[str] = mapped_column(default=None)
    Avg_salary: Mapped[int] =  mapped_column()

    # likes by users (many to many)
    liked_by: Mapped[List[User]] = relationship(
        secondary=roles_liked_by_user, back_populates="liked_roles"
    )

    # creator information (many to one )
    creator_id: Mapped[int] = mapped_column(ForeignKey("contributors.id"))
    creator: Mapped[User] = relationship(back_populates="created_roles")

    #skilled required for role ( many to many )
    required_skills: Mapped[List[Skill]] = relationship(
        secondary=role_skill, back_populates="roles_for_skill"
    )

    # courses for role ( many to many )
    courses_for_role: Mapped[List[Course]] = relationship(
        secondary=role_course, back_populates="target_roles"
    )

    # education required for role
    education: Mapped[List[Education]] = relationship(
        secondary=role_education, back_populates="roles"
    )

    # type of the role
    type_id:Mapped[int] = mapped_column(ForeignKey("role_type.id"))
    type: Mapped[RoleType] = relationship(back_populates= "roles")



class Course(Base):

    __tablename__ = "courses"
    __table_args__ = {'extend_existing': True}
    
    # information
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String,unique= True)
    link: Mapped[str] = mapped_column(unique=True)
    duration_hours:Mapped[int]  = mapped_column() 
    is_free: Mapped[bool] = mapped_column()

    # relationships
    liked_by:Mapped[List[User]]= relationship(
        secondary = courses_liked_by_user, back_populates = "liked_courses"
    )
    #creator information
    creator_id: Mapped[int] = mapped_column(ForeignKey("contributors.id"))
    creator: Mapped[User] = relationship(back_populates="created_courses")

    # role that will be achieved
    target_roles: Mapped[List[Role]] = relationship(
        secondary=role_course,back_populates="courses_for_role"
    )
    
    #course will give these skill
    target_skill: Mapped[List[Skill]] = relationship(
        secondary=skill_course,back_populates="courses_for_skill"
    )

    #prerequisite skills
    skills_required : Mapped[List[Skill]] = relationship()

    #language of course
    language: Mapped[List[Language]] = relationship()
    


class Skill(Base):

    __tablename__ = "skills"
    __table_args__ = {'extend_existing': True}

    # information
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String,unique= True)
    description: Mapped[str] = mapped_column(default=None)

    # relationships
    liked_by: Mapped[List[User]] = relationship(
        secondary= skills_liked_by_user, back_populates="liked_skills"
    )
    creator_id: Mapped[int] = mapped_column(ForeignKey("contributors.id"))
    creator: Mapped[User] = relationship(back_populates="created_skills")

    roles_for_skill: Mapped[List[Role]] = relationship(
        secondary=role_skill, back_populates="required_skills"
    )


    courses_for_skill: Mapped[List[Course]] = relationship(
        secondary=skill_course, back_populates="target_skill"
    )




class RoleType(Base):

    __tablename__ = "role_type"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    roles:Mapped[List[Role]] = relationship(back_populates="type")

class Education(Base):

    __tablename__ = "education"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    duration_year: Mapped[int] = mapped_column()

    # roles for the education
    roles: Mapped[List[Role]] = relationship(
        secondary=role_education, back_populates="education"
    )

class Language(Base):

    __tablename__ = "languages"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
     