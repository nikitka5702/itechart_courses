from django.contrib import admin

from app.models import Student, Teacher, Mark

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Mark)
