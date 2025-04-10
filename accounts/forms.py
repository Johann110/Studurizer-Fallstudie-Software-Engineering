from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User

class UserLoginForm(forms.Form):
    """
    Form for user login
    """
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your username'),
            'aria-label': _('Username'),
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password'),
            'aria-label': _('Password'),
        })
    )

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users. Only for admin use.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'matriculation_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add accessibility attributes
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'aria-label': field.label,
            })

class UserProfileForm(forms.ModelForm):
    """
    Form for users to update their profile
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile_picture')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add accessibility attributes
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'aria-label': field.label,
            })
