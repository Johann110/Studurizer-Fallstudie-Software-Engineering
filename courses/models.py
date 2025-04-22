from django.db import models
from accounts.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(verbose_name="Enddatum")
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses', verbose_name="Studierende Teilnehmer")
    teachers = models.ManyToManyField(CustomUser, related_name='teaching_courses', verbose_name="Dozierende Teilnehmer")

    def __str__(self):
        return self.title
