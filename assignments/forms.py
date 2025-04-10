from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.utils import timezone

from .models import Assignment, Submission, Grade
from documents.models import Document

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class AssignmentForm(forms.ModelForm):
    """
    Form for creating and updating assignments
    """
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'max_points', 'due_date', 
                  'is_active', 'allow_late_submissions', 'late_penalty_percentage',
                  'related_documents']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Assignment title'),
                'aria-label': _('Title'),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Assignment instructions'),
                'aria-label': _('Description'),
            }),
            'max_points': forms.NumberInput(attrs={
                'class': 'form-control',
                'aria-label': _('Maximum points'),
            }),
            'due_date': DateTimeInput(attrs={
                'class': 'form-control',
                'aria-label': _('Due date'),
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'aria-label': _('Active'),
            }),
            'allow_late_submissions': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'allow_late',
                'aria-label': _('Allow late submissions'),
            }),
            'late_penalty_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'data-depends-on': 'allow_late',
                'data-depends-value': 'true',
                'aria-label': _('Late penalty percentage'),
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        
        # Filter related documents by course
        if self.course:
            self.fields['related_documents'].queryset = Document.objects.filter(course=self.course)
            self.fields['related_documents'].widget = forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
                'aria-label': _('Related documents'),
            })
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        
        # Ensure due date is in the future for new assignments
        if not self.instance.pk and due_date and due_date < timezone.now():
            raise forms.ValidationError(_('Due date must be in the future'))
        
        return due_date
    
    def clean(self):
        cleaned_data = super().clean()
        allow_late = cleaned_data.get('allow_late_submissions')
        
        if allow_late:
            late_penalty = cleaned_data.get('late_penalty_percentage')
            
            if late_penalty is None:
                self.add_error('late_penalty_percentage', _('Please specify a late penalty percentage'))
            elif late_penalty > 100:
                self.add_error('late_penalty_percentage', _('Late penalty cannot exceed 100%'))
        
        return cleaned_data


class SubmissionForm(forms.ModelForm):
    """
    Form for student assignment submissions
    """
    class Meta:
        model = Submission
        fields = ['file', 'text_content']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'aria-label': _('File upload'),
            }),
            'text_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': _('Type your submission here (for text submissions)'),
                'aria-label': _('Text content'),
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        text_content = cleaned_data.get('text_content')
        
        # Validate that at least one submission type is provided
        if not file and not text_content:
            raise forms.ValidationError(_('Please provide either a file or text content for your submission'))
        
        # Validate file size (10 MB limit)
        if file and file.size > 10 * 1024 * 1024:
            self.add_error('file', _('File size cannot exceed 10 MB'))
        
        return cleaned_data


class GradeForm(forms.ModelForm):
    """
    Form for grading student submissions
    """
    class Meta:
        model = Grade
        fields = ['points', 'feedback']
        widgets = {
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'aria-label': _('Points'),
                'step': '0.01',
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Provide feedback for the student'),
                'aria-label': _('Feedback'),
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get max points from submission's assignment
        if self.instance.pk:
            # For existing grades
            max_points = self.instance.submission.assignment.max_points
        elif 'submission' in kwargs.get('initial', {}):
            # For new grades with initial submission data
            submission = kwargs['initial']['submission']
            max_points = submission.assignment.max_points
        else:
            # Default
            max_points = 100
        
        self.fields['points'].validators.append(MaxValueValidator(max_points))
        self.fields['points'].help_text = _('Maximum: {0}').format(max_points)
    
    def clean_points(self):
        points = self.cleaned_data.get('points')
        
        # Add validators for specific instance
        if hasattr(self, 'instance') and hasattr(self.instance, 'submission'):
            max_points = self.instance.submission.assignment.max_points
            if points > max_points:
                raise forms.ValidationError(
                    _('Points cannot exceed the maximum of {0}').format(max_points)
                )
        
        return points
