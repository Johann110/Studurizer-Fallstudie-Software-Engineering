from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import CustomUser, UserProfile

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


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'description', 'signature')
        widgets = {
            'profile_picture': forms.FileInput(),
            'signature': forms.FileInput(),
            'description': forms.Textarea(attrs={
                'placeholder': 'Beschreibe dich!',
                'rows': 4,
                'maxlength': 500,
            }),
        }

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Die Größe der Bilddatei sollte 5 MB nicht überschreiten.')

            file_name = profile_picture.name
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = file_name[file_name.rfind('.'):].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError('Nicht unterstützte Dateierweiterung. Bitte verwenden Sie .jpg, .jpeg, .png, oder .gif')

        return profile_picture

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) > 500:
            raise forms.ValidationError('Beschreibung darf nicht größer sein als 500 Zeichen.')
        return description

    def clean_signature(self):
        signature = self.cleaned_data.get('signature')
        if signature:
            if signature.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Die Größe der Bilddatei sollte 5 MB nicht überschreiten.')

            file_name = signature.name
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = file_name[file_name.rfind('.'):].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError('Nicht unterstützte Dateierweiterung. Bitte verwenden Sie .jpg, .jpeg, .png, oder .gif')

        return signature

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
