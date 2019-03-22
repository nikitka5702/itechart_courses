from django.urls import path

from app.views import (
    IndexView, StudentView, TeacherView,
    StudentCreateView, StudentEditView, StudentDeleteView,
    TeacherCreateView, TeacherEditView, TeacherDeleteView,
    MarkStudentCreate, MarkTeacherCreate,
    info
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('student/<int:pk>', StudentView.as_view(), name='student'),
    path('student/create', StudentCreateView.as_view(), name='student_create'),
    path('student/edit/<int:pk>', StudentEditView.as_view(), name='student_edit'),
    path('student/delete/<int:pk>', StudentDeleteView.as_view(), name='student_delete'),
    path('mark/student/<int:student>', MarkStudentCreate.as_view(), name='mark_student'),
    path('teacher/<int:pk>', TeacherView.as_view(), name='teacher'),
    path('teacher/create', TeacherCreateView.as_view(), name='teacher_create'),
    path('teacher/edit/<int:pk>', TeacherEditView.as_view(), name='teacher_edit'),
    path('teacher/delete/<int:pk>', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('mark/teacher/<int:teacher>', MarkTeacherCreate.as_view(), name='mark_teacher'),
    path('info/', info, name='info')
]
