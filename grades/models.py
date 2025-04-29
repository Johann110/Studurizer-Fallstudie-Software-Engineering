from django.db import models

from accounts.models import CustomUser
from submissions.models import Submission


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.SET_NULL, null=True, blank=True, related_name='grade')
    feedback = models.TextField(max_length=100)
    grade = models.CharField(max_length=20)
