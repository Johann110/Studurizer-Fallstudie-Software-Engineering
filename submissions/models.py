import os
import shutil

from django.db import models

from StudurizerApp import settings
from assignments.models import Assignment
from accounts.models import CustomUser
#from grades.models import Grade


def submission_file_upload_path(instance, filename):
    return f'submissions/user_{instance.user.id}/assignment_{instance.assignment.id}/{filename}'


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions')
    #grade = models.OneToOneField(Grade, on_delete=models.SET_NULL, null=True, blank=True)

    file = models.FileField(upload_to=submission_file_upload_path)

    agreed_to_data_policy = models.BooleanField(default=False)
    submitted_statutory_declaration = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)

        if self.statutory_declaration_file and os.path.isfile(self.statutory_declaration_file.path):
            os.remove(self.statutory_declaration_file.path)

        submission_folder = os.path.join(
            settings.MEDIA_ROOT, f'submissions/user_{self.user.id}/assignment_{self.assignment.id}/'
        )
        if os.path.isdir(submission_folder):
            shutil.rmtree(submission_folder, ignore_errors=True)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Submission by {self.user.username} for {self.assignment.title}'
