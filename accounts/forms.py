from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import CustomUser


class CustomUserAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    class Meta:
        model = CustomUser
        fields = ('password')