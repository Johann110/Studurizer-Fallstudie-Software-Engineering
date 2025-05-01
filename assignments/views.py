import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DeleteView

from assignments.forms import AssignmentForm
from assignments.models import AssignmentFile, Assignment
from courses.models import Course
from grades.models import Grade
from submissions.models import Submission


def create_assignment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            for key, file in request.FILES.items():
                AssignmentFile.objects.create(
                    assignment=assignment,
                    file=file,
                )
            return redirect('course_detail', pk=course.id)
    else:
        form = AssignmentForm()

    context = {
        'form': form,
        'course': course,
    }

    return render(request, 'assignments/create_assignment.html', context)


class DeleteAssignment(DeleteView):
    model = Assignment

    def get_success_url(self):
        course_id = self.object.course.id
        return reverse('course_detail', args=[course_id])


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    try:
        user_submission = Submission.objects.get(assignment=assignment, user=request.user)
        grade = Grade.objects.filter(submission=user_submission).first()
    except:
        user_submission = None
        grade = None
    assignment.check_and_close()
    files = assignment.files.all()
    course = assignment.course
    context = {
        'course': course,
        'submissions': submissions,
        'user_submission': user_submission,
        'grade': grade,
        'files': files,
        'assignment': assignment,
    }

    return render(request, 'assignments/assignment_detail.html', context)


def update_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        # Quelle: Codegenerierung mit ChatGPT
        if form.is_valid():
            # have to be in this order otherwise it wont work with the dropzone
            assignment = form.save(commit=False)
            assignment.save()
            for key, file in request.FILES.items():
                AssignmentFile.objects.create(
                    assignment=assignment,
                    file=file,
                )
            return redirect('home')
        # Ende der Generierung
        else:
            form = AssignmentForm(instance=assignment)
            files = assignment.files.all()

            context = {
                'form': form,
                'assignment': assignment,
                'files': files,
            }

            return render(request, 'courses/update_course.html', context)
    elif request.method == 'GET':
        form = AssignmentForm(instance=assignment)
        files = assignment.files.all()

        context = {
            'form': form,
            'assignment': assignment,
            'files': files
        }

        return render(request, 'assignments/update_assignment.html', context)
    return HttpResponse("Nur POST oder GET erlaubt", status=405)


def delete_assignment_file(request, file_id):
    file = get_object_or_404(AssignmentFile, pk=file_id)

    if file.file and file.file.path and os.path.isfile(file.file.path):
        os.remove(file.file.path)

    file.delete()

    return JsonResponse({'success': True})
