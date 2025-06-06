import os
import shutil

from django.db import models
from django.utils import timezone

from StudurizerApp import settings


class Assignment(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255,verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    start_time = models.DateTimeField(verbose_name="Startzeit")
    end_time = models.DateTimeField(verbose_name="Endzeit")
    is_open = models.BooleanField(default=True,verbose_name="Offen")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Erzeugt am")

    def delete(self, *args, **kwargs):
        assignment_folder = os.path.join(settings.MEDIA_ROOT, f'courses/course_{self.course.id}/assignments/{self.id}')

        for file in self.files.all():
            if file.file and os.path.isfile(file.file.path):
                os.remove(file.file.path)
            file.delete()

        if os.path.exists(assignment_folder):
            shutil.rmtree(assignment_folder, ignore_errors=True)

        super().delete(*args, **kwargs)

    # im view:
    # assignment = Assignment.objects.get(pk=assignment_id)
    # assignment.check_and_close()
    def check_and_close(self):
        if self.is_open and timezone.now() > self.end_time:
            self.is_open = False
            self.save(update_fields=['is_open'])

    def __str__(self):
        return self.title


def assignment_file_upload_path(instance, filename):
    return f'courses/course_{instance.assignment.course.id}/assignments/{instance.assignment.id}/{filename}'


class AssignmentFile(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=assignment_file_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.file.name}"
