from django.shortcuts import render, get_object_or_404, redirect

from assignments.forms import AssignmentForm
from assignments.models import AssignmentFile, Assignment
from courses.models import Course


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


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    assignment.check_and_close()
    files = assignment.files.all()
    course = assignment.course

    context = {
        'course': course,
        'files': files,
        'assignment': assignment,
    }

    return render(request, 'assignments/assignment_detail.html', context)