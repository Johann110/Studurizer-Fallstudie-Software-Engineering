from django import forms

from accounts.models import CustomUser
from courses.models import Course


class CourseForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(groups__name="Student").distinct(),
        widget=forms.SelectMultiple(attrs={'class': 'dual-listbox-student', 'size': '10'}),
        required=False,
        label="Teilnehmende (Studierende)"
    )

    teachers = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(groups__name="Teacher").distinct(),
        widget=forms.SelectMultiple(attrs={'class': 'dual-listbox-teacher', 'size': '10'}),
        required=False,
        label="Lehrkräfte"
    )

    class Meta:
        model = Course
        fields = '__all__'
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}),
                   'end_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
