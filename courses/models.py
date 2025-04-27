import os
import shutil

from django.db import models

from StudurizerApp import settings
from accounts.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(verbose_name="Enddatum")
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses', verbose_name="Studierende Teilnehmer")
    teachers = models.ManyToManyField(CustomUser, related_name='teaching_courses', verbose_name="Dozierende Teilnehmer")

    # Quelle: Codegenerierung mit Grok3
    def delete(self, *args, **kwargs):
        course_folder = os.path.join(settings.MEDIA_ROOT, f'course_{self.id}')

        for material in self.materials.all():
            if material.file and os.path.isfile(material.file.path):
                os.remove(material.file.path)
            material.delete()

        if os.path.exists(course_folder):
            shutil.rmtree(course_folder, ignore_errors=True)

        super().delete(*args, **kwargs)
    # Ende der Generierung

    def __str__(self):
        return self.title
