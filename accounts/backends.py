from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                raise ValidationError("Password doesn't match")
        except CustomUser.DoesNotExist:
            return None