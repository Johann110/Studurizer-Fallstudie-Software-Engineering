from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile

class UserProfileForm(forms.ModelForm):
    """
    Form for users to update their profile
    """
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'description')
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'aria-label': _('Profile picture'),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Tell us about yourself (maximum 500 characters)'),
                'aria-label': _('Description'),
                'rows': 4,
                'maxlength': 500,
            }),
        }
        
    def clean_profile_picture(self):
        """Validate profile picture format and size"""
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Check file size (limit to 5MB)
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError(_('Image file size should not exceed 5MB.'))
            
            # Check file extension
            file_name = profile_picture.name
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = file_name[file_name.rfind('.'):].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(_('Unsupported file extension. Please use .jpg, .jpeg, .png, or .gif.'))
                
        return profile_picture
    
    def clean_description(self):
        """Validate description length"""
        description = self.cleaned_data.get('description')
        if description and len(description) > 500:
            raise forms.ValidationError(_('Description cannot exceed 500 characters.'))
        return description
