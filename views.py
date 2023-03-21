from sqladmin import ModelView
import models

class User(ModelView,model = models.User ):
    column_list = [
        models.User.id,
        models.User.name,
        models.User.email,
        models.User.contributor
        ]

class Contributor(ModelView,model = models.Contributor):
    column_list = [
        models.Contributor.id,
        models.Contributor.user,
        models.Contributor.description,
        models.Contributor.created_courses,
        models.Contributor.created_roles,
        models.Contributor.created_skills,
    ]

class Role(ModelView,model = models.Role):
    column_list = [
        models.Role.id,
        models.Role.name,
        models.Role.description,
        models.Role.avg_salary,
        models.Role.liked_by,
        models.Role.creator_id,
        models.Role.creator,
        models.Role.required_skills,
        models.Role.courses_for_role,
        models.Role.education,
        models.Role.type,
        models.Role.type_id,
    ]

class Course(ModelView,model =  models.Course):
    column_list = [
        models.Course.id,
        models.Course.name,
        models.Course.link,
        models.Course.duration_hours,
        models.Course.is_free,
        models.Course.liked_by,
        models.Course.creator_id,
        models.Course.creator,
        models.Course.target_roles,
        models.Course.target_skill,
        models.Course.skills_required,
        models.Course.languages,
    ]

class Skill(ModelView, model = models.Skill):
    column_list = [
        models.Skill.id,
        models.Skill.name,
        models.Skill.description,
        models.Skill.creator_id,
        models.Skill.liked_by,
        models.Skill.creator,
        models.Skill.roles_for_skill,
        models.Skill.courses_for_skill,
        models.Skill.further_courses,

    ]

class RoleType(ModelView, model = models.RoleType):
    column_list = [
        models.RoleType.id,
        models.RoleType.name,
        models.RoleType.roles,
    ]

class Education(ModelView,model = models.Education):
    column_list = [
        models.Education.id,
        models.Education.name,
        models.Education.duration_year,
        models.Education.roles,
    ]


class Language(ModelView, model = models.Language):
    column_list = [
        models.Language.id,
        models.Language.name,
        models.Language.courses,

    ]