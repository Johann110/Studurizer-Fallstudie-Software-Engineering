
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from grades.forms import GradeForm
from grades.models import Grade
from submissions.models import Submission
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import FileResponse, Http404
import os
from django.conf import settings


class CreateGradeForSubmission(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grades/create_grade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_id = self.kwargs.get('submission_id')
        submission = get_object_or_404(Submission, pk=submission_id)
        context['submission'] = submission
        context['student'] = submission.user
        return context

    def form_valid(self, form):
        submission_id = self.kwargs.get('submission_id')
        submission = get_object_or_404(Submission, pk=submission_id)
        form.instance.submission = submission

        # Erfolgsform speichern
        return super().form_valid(form)

    def get_success_url(self):
        submission = get_object_or_404(Submission, pk=self.kwargs["submission_id"])
        assignment_id = submission.assignment.id
        return reverse_lazy("assignment_detail", kwargs={"assignment_id": assignment_id})



@xframe_options_exempt
def embedded_pdf_view(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, 'rb'), content_type='application/pdf')
    raise Http404("Datei nicht gefunden.")


class UpdateGradeForSubmission(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grades/update_grade.html'

    def get_object(self, queryset=None):
        submission_id = self.kwargs.get('submission_id')
        submission = get_object_or_404(Submission, pk=submission_id)
        return get_object_or_404(Grade, submission=submission)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_id = self.kwargs.get('submission_id')
        submission = get_object_or_404(Submission, pk=submission_id)
        context['submission'] = submission
        context['student'] = submission.user
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        submission = get_object_or_404(Submission, pk=self.kwargs["submission_id"])
        assignment_id = submission.assignment.id
        return reverse_lazy("assignment_detail", kwargs={"assignment_id": assignment_id})
