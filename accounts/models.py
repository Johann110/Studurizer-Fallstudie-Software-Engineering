from django.contrib.auth.models import User
from django.db import models

class CustomUser(User):
    email = models.EmailField(verbose_name="Email", unique=True)

class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Nutzer", on_delete=models.CASCADE, related_name="Nutzer")
    profile_picture = models.ImageField(upload_to='profile_pictures/', verbose_name="Profilbild")
    description = models.TextField(verbose_name="Beschreibung",)
