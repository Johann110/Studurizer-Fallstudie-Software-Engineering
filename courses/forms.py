from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Course, Session

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CourseForm(forms.ModelForm):
    """
    Form for creating and updating courses
    """
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': DateInput(attrs={'aria-label': _('Start date')}),
            'end_date': DateInput(attrs={'aria-label': _('End date')}),
            'description': forms.Textarea(attrs={'rows': 5, 'aria-label': _('Description')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add accessibility attributes
        for field_name, field in self.fields.items():
            if 'aria-label' not in field.widget.attrs:
                field.widget.attrs.update({
                    'aria-label': field.label,
                })
            field.widget.attrs.update({
                'class': 'form-control',
            })
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_('End date must be after start date'))
        
        return cleaned_data

class SessionForm(forms.ModelForm):
    """
    Form for creating and updating course sessions
    """
    class Meta:
        model = Session
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 
                 'is_online', 'location', 'online_meeting_link']
        widgets = {
            'date': DateInput(attrs={'aria-label': _('Date')}),
            'start_time': TimeInput(attrs={'aria-label': _('Start time')}),
            'end_time': TimeInput(attrs={'aria-label': _('End time')}),
            'description': forms.Textarea(attrs={'rows': 5, 'aria-label': _('Description')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add accessibility attributes
        for field_name, field in self.fields.items():
            if 'aria-label' not in field.widget.attrs:
                field.widget.attrs.update({
                    'aria-label': field.label,
                })
            field.widget.attrs.update({
                'class': 'form-control',
            })
            
            # Handle conditional fields
            if field_name == 'location':
                field.widget.attrs.update({
                    'data-depends-on': 'is_online',
                    'data-depends-value': 'false',
                })
            elif field_name == 'online_meeting_link':
                field.widget.attrs.update({
                    'data-depends-on': 'is_online',
                    'data-depends-value': 'true',
                })
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        is_online = cleaned_data.get('is_online')
        location = cleaned_data.get('location')
        online_meeting_link = cleaned_data.get('online_meeting_link')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(_('End time must be after start time'))
        
        if is_online and not online_meeting_link:
            self.add_error('online_meeting_link', _('Online meeting link is required for online sessions'))
        
        if not is_online and not location:
            self.add_error('location', _('Location is required for in-person sessions'))
        
        return cleaned_data