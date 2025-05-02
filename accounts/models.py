from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="Email", unique=True)


def signature_file_upload_path(instance, filename):
    return f'signatures/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Nutzer", on_delete=models.CASCADE, related_name="Nutzer")
    profile_picture = models.ImageField(upload_to='profile_pictures/', verbose_name="Profilbild")
    description = models.TextField(verbose_name="Beschreibung",)
    signature = models.ImageField(
        upload_to=signature_file_upload_path,
        verbose_name="Unterschrift",
        blank=True,
        null=True
    )
