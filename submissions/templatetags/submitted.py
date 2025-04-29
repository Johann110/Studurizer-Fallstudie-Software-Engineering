from django import template
from django.contrib.auth.models import User

from assignments.models import Assignment
from submissions.models import Submission

register = template.Library()


@register.filter(name='has_submitted')
def has_submitted(user : User, assignment : int) -> bool:
    submissions = Submission.objects.filter(user=user)
    for submission in submissions:
        if submission.assignment_id == assignment:
            return True
    return False