from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from courses.forms import CourseForm
from courses.models import Course
from material.models import Material


def create_course(request):
    # Quelle: Codegenerierung mit ChatGPT
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            # have to be in this order otherwise it wont work with the dropzone
            course = form.save(commit=False)
            course.save()
            form.save_m2m()
            for key, file in request.FILES.items():
                Material.objects.create(
                    course=course,
                    file=file,
                    uploaded_by=request.user
                )
            return redirect('home')
    # Ende der Generierung
        else:
            form = CourseForm()

            context = {
                'form': form,
            }

            return render(request, 'courses/update_course.html', context)
    elif request.method == 'GET':
        form = CourseForm()

        context = {
            'form': form
        }

        return render(request, 'courses/create_course.html', context)
    return HttpResponse("Nur POST oder GET erlaubt", status=405)


def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        # Quelle: Codegenerierung mit ChatGPT
        if form.is_valid():
            # have to be in this order otherwise it wont work with the dropzone
            course = form.save(commit=False)
            course.save()
            form.save_m2m()
            for key, file in request.FILES.items():
                Material.objects.create(
                    course=course,
                    file=file,
                    uploaded_by=request.user
                )
            return redirect('home')
        # Ende der Generierung
        else:
            form = CourseForm(instance=course)
            files = course.materials.all()

            context = {
                'form': form,
                'course': course,
                'files': files,
            }

            return render(request, 'courses/update_course.html', context)
    elif request.method == 'GET':
        form = CourseForm(instance=course)
        files = course.materials.all()

        context = {
            'form': form,
            'course': course,
            'files': files
        }

        return render(request, 'courses/update_course.html', context)
    return HttpResponse("Nur POST oder GET erlaubt", status=405)


class DeleteCourse(DeleteView):
    model = Course
    success_url = reverse_lazy('home')


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    files = course.materials.all()
    assignments = course.assignments.all()

    # Check and close assignments if end datetime reached
    for assignment in assignments:
        assignment.check_and_close()

    context = {
        'course': course,
        'files': files,
        'assignments': assignments,
    }

    return render(request, 'courses/course_detail.html', context)