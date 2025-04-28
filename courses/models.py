import os
import shutil

from django.db import models

from StudurizerApp import settings
from accounts.models import CustomUser
from assignments.models import Assignment


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    start_date = models.DateField(verbose_name="Startdatum")
    end_date = models.DateField(verbose_name="Enddatum")
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses', verbose_name="Studierende Teilnehmer")
    teachers = models.ManyToManyField(CustomUser, related_name='teaching_courses', verbose_name="Dozierende Teilnehmer")

    # Quelle: Codegenerierung mit Grok3
    def delete(self, *args, **kwargs):
        course_folder = os.path.join(settings.MEDIA_ROOT, f'courses/course_{self.id}')

        # delete all materials associated with the course
        for material in self.materials.all():
            if material.file and os.path.isfile(material.file.path):
                os.remove(material.file.path)
            material.delete()

        # delete all assignments associated with the course
        for assignment in self.assignments.all():
            assignment_folder = os.path.join(settings.MEDIA_ROOT, f'courses/course_{assignment.course.id}/assignments/{assignment.id}')
            for file in assignment.files.all():
                if file.file and os.path.isfile(file.file.path):
                    os.remove(file.file.path)
                file.delete()
            if os.path.exists(assignment_folder):
                shutil.rmtree(assignment_folder, ignore_errors=True)
            assignment.delete()

        # delete course folder
        if os.path.exists(course_folder):
            shutil.rmtree(course_folder, ignore_errors=True)

        super().delete(*args, **kwargs)
    # Ende der Generierung

    def __str__(self):
        return self.title
