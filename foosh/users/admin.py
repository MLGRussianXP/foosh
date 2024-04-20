from django.contrib import admin

from users.models import School, Student


__all__ = []


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        School.user.field.name,
        School.name.field.name,
        School.city.field.name,
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        Student.user.field.name,
        Student.name.field.name,
        Student.surname.field.name,
        Student.patronymic.field.name,
        Student.city.field.name,
        Student.school.field.name,
    )
