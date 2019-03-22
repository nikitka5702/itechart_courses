from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from app.models import Student, Teacher, Mark


# Create your views here.
def info(request):
    return render(request, 'app/info.html', {})


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html', {'students': Student.objects.all(), 'teachers': Teacher.objects.all()})


class StudentView(DetailView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg'] = context['object'].marks.aggregate(avg=Avg('mark')).get('avg') or .0
        return context


class StudentCreateView(CreateView):
    model = Student
    fields = (
        'name',
        'surname',
        'birth_date'
    )


class StudentEditView(UpdateView):
    model = Student
    fields = (
        (
            'name',
            'surname',
            'birth_date'
        )
    )


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'app/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('index')


class TeacherView(DetailView):
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg'] = context['object'].marks.aggregate(avg=Avg('mark')).get('avg') or .0
        return context


class TeacherCreateView(CreateView):
    model = Teacher
    fields = (
        'name',
        'surname',
        'position'
    )


class TeacherEditView(UpdateView):
    model = Teacher
    fields = (
        (
            'name',
            'surname',
            'position'
        )
    )


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'app/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('index')


class MarkStudentCreate(CreateView):
    model = Mark
    fields = (
        'subject',
        'mark',
        'teacher'
    )

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs.get('student'))
        teacher = form.cleaned_data['teacher']
        marks = teacher.marks.filter(student=student).count()
        if marks == 3:
            form.add_error('teacher', 'Selected teacher cannot add any more marks to this student')
            return super().form_invalid(form)
        form.instance.student = student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student', kwargs={'pk': self.object.student.pk})


class MarkTeacherCreate(CreateView):
    model = Mark
    fields = (
        'subject',
        'mark',
        'student'
    )

    def form_valid(self, form):
        teacher = get_object_or_404(Teacher, pk=self.kwargs.get('teacher'))
        student = form.cleaned_data['student']
        marks = student.marks.filter(teacher=teacher).count()
        if marks == 3:
            form.add_error('student', 'You cannot add any more marks to this student')
            return super().form_invalid(form)
        form.instance.teacher = teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacher', kwargs={'pk': self.object.teacher.pk})
