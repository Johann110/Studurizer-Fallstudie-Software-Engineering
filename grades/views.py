
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

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
        course_id = submission.assignment.course.id
        return reverse_lazy("course_detail", kwargs={"pk": course_id})



@xframe_options_exempt
def embedded_pdf_view(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, 'rb'), content_type='application/pdf')
    raise Http404("Datei nicht gefunden.")
