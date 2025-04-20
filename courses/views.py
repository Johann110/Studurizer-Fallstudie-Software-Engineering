from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from courses.forms import CourseForm
from courses.models import Course


# Create your views here.
class CreateCourse(CreateView):
    model = Course
    template_name = 'courses/create_course.html'
    form_class = CourseForm
    success_url = reverse_lazy("home")


class UpdateCourse(UpdateView):
    model = Course
    template_name = 'courses/update_course.html'
    form_class = CourseForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'pk'


class DeleteCourse(DeleteView):
    model = Course
    success_url = reverse_lazy('home')


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})