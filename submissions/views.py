from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .models import Submission
from assignments.models import Assignment
from .forms import SubmissionForm


# def create_submission(request, assignment_id):
#     assignment = get_object_or_404(Assignment, pk=assignment_id)
#
#     if request.method == 'POST':
#         form = SubmissionForm(request.POST, request.FILES)
#         if form.is_valid():
#             submission = form.save(commit=False)
#             submission.assignment = assignment
#             submission.user = request.user
#             submission.save()
#             return redirect('assignment_detail', assignment_id=assignment.id)
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)
#
#     else:
#         form = SubmissionForm()
#
#     context = {
#         'form': form,
#         'assignment': assignment,
#     }
#     return render(request, 'submissions/create_submission.html', context)

def create_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':

        if not assignment.is_open:
            return JsonResponse({
                'success': False,
                'message': 'Die Abgabefrist ist abgelaufen.'
            }, status=400)

        print(request.POST)
        print(request.FILES)

        agreed_to_data_policy = request.POST.get('agreed_to_data_policy') == 'true'
        submitted_statutory_declaration = request.POST.get('submitted_statutory_declaration') == 'true'

        if not agreed_to_data_policy or not submitted_statutory_declaration:
            return JsonResponse({
                'success': False,
                'message': 'Sie müssen die Datenschutzrichtlinie und die Eidesstattliche akzeptieren um abgeben zu können.'
            }, status=400)

        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'message': 'Es wurde keine Datei hochgeladen.'
            }, status=400)

        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.user = request.user
            submission.agreed_to_data_policy = agreed_to_data_policy
            submission.submitted_statutory_declaration = submitted_statutory_declaration
            submission.save()
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('assignment_detail', kwargs={'assignment_id': assignment.id})
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Fehler im Formular.',
                'errors': form.errors
            }, status=400)

    form = SubmissionForm()
    context = {
        'form': form,
        'assignment': assignment,
    }
    return render(request, 'submissions/create_submission.html', context)