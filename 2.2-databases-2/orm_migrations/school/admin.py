from django.contrib import admin

from .models import Student, Teacher

class GroupInline(admin.TabularInline):
    model = Student.teacher.through
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
    inlines = [GroupInline]



@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    inlines = [GroupInline]
