from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
