from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'
        exclude = ['assignment', 'user', 'created_at']

        widgets = {
            'agreed_to_terms_of_condition': forms.CheckboxInput(),
            'agreed_to_data_policy': forms.CheckboxInput(),
            'submitted_statutory_declaration': forms.CheckboxInput(),
        }