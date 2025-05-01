from django import forms
from .models import Grade
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['feedback', 'grade']
        widgets = {
            'feedback': forms.Textarea(),
            'grade': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()