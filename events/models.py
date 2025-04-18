from django.db import models

from courses.models import Course


# Create your models here.
class Events(models.Model):
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name='Kurs',
        null=True,
        blank=True
    )