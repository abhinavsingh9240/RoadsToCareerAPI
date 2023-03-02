from __future__ import annotations

from sqlalchemy import Column,String
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List

from database import Base



career_skill = Table(
    "career_skill",
    Base.metadata,
    Column("career_id", ForeignKey("careers.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
)

career_course = Table(
    "career_course",
    Base.metadata,
    Column("career_id",ForeignKey("careers.id"),primary_key=True),
    Column("course_id",ForeignKey("courses.id"),primary_key = True)
)

skill_course = Table(
    "skill_course",
    Base.metadata,
    Column("skill_id",ForeignKey("skills.id"),primary_key=True),
    Column("course_id",ForeignKey("courses.id"),primary_key = True)
)


class Career(Base):
    __tablename__ = "careers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String,unique= True)
    requirements: Mapped[List[Skill]] = relationship(
        secondary=career_skill, back_populates="target"
    )
    courses_for_career: Mapped[List[Course]] = relationship(
        secondary=career_course, back_populates="target_career"
    )



class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String,unique= True)
    target: Mapped[List[Career]] = relationship(
        secondary=career_skill, back_populates="requirements"
    )
    courses_for_skill: Mapped[List[Course]] = relationship(
        secondary=skill_course, back_populates="target_skill"
    )

class Course(Base):

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String,unique= True)
    target_career: Mapped[List[Career]] = relationship(
        secondary=career_course,back_populates="courses_for_career"
    )
    target_skill: Mapped[List[Skill]] = relationship(
        secondary=skill_course,back_populates="courses_for_skill"
    )