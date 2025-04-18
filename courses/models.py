from django.db import models
from accounts.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses')
    teachers = models.ManyToManyField(CustomUser, related_name='teaching_courses')
