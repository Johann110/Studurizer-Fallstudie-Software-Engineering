from django.db import models

from courses.models import Course


class Events(models.Model):
    description = models.TextField(verbose_name="Beschreibung")
    start_date = models.DateTimeField(verbose_name="Startzeit")
    end_date = models.DateTimeField(verbose_name="Endzeit")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name='Kurs',
        null=True,
        blank=True,
        verbose_name="Kurs",
    )
    def __str__(self):
        return self.description