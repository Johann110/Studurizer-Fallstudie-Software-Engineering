from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from courses.forms import CourseForm
from courses.models import Course
from material.models import Material


# Create your views here.
class CreateCourse(CreateView):
    model = Course
    template_name = 'courses/create_course.html'
    form_class = CourseForm
    success_url = reverse_lazy("home")


# class UpdateCourse(UpdateView):
#     model = Course
#     template_name = 'courses/update_course.html'
#     form_class = CourseForm
#     success_url = reverse_lazy("home")

def update_course(request, pk):
    print(request.POST)
    print(request.FILES)
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        print("aktueller kurs ausgewählt:", course.title)
        if form.is_valid():
            course = form.save()
            print("POST-Daten:", request.POST)
            print("FILES:", request.FILES)
            for key, file in request.FILES.items():
                print(f"Datei-Feld: {key}, Dateiname: {file.name}, Größe: {file.size}")
                Material.objects.create(
                    course=course,
                    file=file,
                    uploaded_by=request.user
                )
            return redirect('home')
        else:
            print("Formular ungültig:", form.errors)
        return JsonResponse({'status': 'received'})
    elif request.method == 'GET':
        form = CourseForm(instance=course)
        return render(request, 'courses/update_course.html', {'form': form, 'course': course})
    return HttpResponse("Nur POST erlaubt", status=405)



class DeleteCourse(DeleteView):
    model = Course
    success_url = reverse_lazy('home')


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})