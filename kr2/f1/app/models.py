from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=127)
    surname = models.CharField(max_length=127)
    birth_date = models.DateField()

    def get_absolute_url(self):
        return reverse('student', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name} {self.surname}"


class Teacher(models.Model):
    name = models.CharField(max_length=127)
    surname = models.CharField(max_length=127)
    position = models.CharField(max_length=127, choices=(
        ('Асп', 'Аспирант'),
        ('Асс', 'Ассистент'),
        ('Доц', 'Доцент'),
        ('Проф', 'Профессор')
    ))

    def get_absolute_url(self):
        return reverse('teacher', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name} {self.surname}"


class Mark(models.Model):
    subject = models.CharField(max_length=127)
    mark = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    created_at = models.DateField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='marks')

    def __str__(self):
        return self.subject
