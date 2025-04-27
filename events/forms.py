from django import forms

from courses.models import Course
from events.models import Events
from django import forms

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['description', 'start_date', 'end_date', 'course']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'course': forms.Select(attrs={
                'class': 'form-select',
                'data-live-search': 'true'
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
        if user:
            self.fields['course'].queryset = Course.objects.filter(teachers=user)
