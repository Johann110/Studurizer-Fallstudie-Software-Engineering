from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from .models import Document
from courses.models import Course, Session

class DocumentUploadForm(forms.ModelForm):
    """
    Form for uploading documents
    """
    session = forms.ModelChoiceField(
        queryset=None,
        required=False,
        help_text=_('Select the session this document belongs to (optional)'),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-label': _('Session'),
        })
    )
    
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'doc_type', 'session', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter document title'),
                'aria-label': _('Title'),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Enter document description (optional)'),
                'aria-label': _('Description'),
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'aria-label': _('File'),
            }),
            'doc_type': forms.Select(attrs={
                'class': 'form-control',
                'aria-label': _('Document type'),
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'aria-label': _('Is public'),
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        
        if self.course:
            # Filter sessions to only show those from this course
            self.fields['session'].queryset = Session.objects.filter(course=self.course).order_by('date', 'start_time')
            
            # If there are no sessions, hide the field
            if not self.fields['session'].queryset.exists():
                self.fields['session'].widget = forms.HiddenInput()
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (10 MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(_('File size cannot exceed 10 MB'))
            
            # Validate file extension
            allowed_extensions = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'zip', 'png', 'jpg', 'jpeg', 'gif']
            validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
            try:
                validator(file)
            except forms.ValidationError:
                raise forms.ValidationError(
                    _('Invalid file type. Allowed types: {0}').format(', '.join(allowed_extensions))
                )
        return file
