from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ['course', 'created_at', 'is_open']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial['start_time'] = self.instance.start_time.strftime('%Y-%m-%dT%H:%M') if self.instance.start_time else ''
        self.initial['end_time'] = self.instance.end_time.strftime('%Y-%m-%dT%H:%M') if self.instance.end_time else ''

        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()