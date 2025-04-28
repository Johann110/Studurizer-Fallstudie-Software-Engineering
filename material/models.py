from django.db import models

from courses.models import Course
from accounts.models import CustomUser


def course_material_upload_path(instance, filename):
    return f'courses/course_{instance.course.id}/material/{filename}'


class Material(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name="Kurs"
    )

    file = models.FileField(
        upload_to=course_material_upload_path,
        verbose_name="Datei"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Hochgeladen am"
    )

    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_materials',
        verbose_name="Hochgeladen von"
    )