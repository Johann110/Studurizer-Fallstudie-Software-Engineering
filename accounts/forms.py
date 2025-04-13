from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import CustomUser

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import CustomUser


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Diese E-Mail-Adresse ist nicht registriert.")

        if not user.check_password(password):
            raise forms.ValidationError("Das eingegebene Passwort ist ungültig.")

        self.user_cache = user
        return self.cleaned_data
