from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from .models import Course, Enrollment, Session
from .forms import CourseForm, SessionForm
from accounts.models import User

@login_required
def dashboard(request):
    """
    Main dashboard view displaying courses for the logged-in user
    """
    user = request.user
    
    if user.is_teacher():
        # For teachers, show the courses they teach
        courses = Course.objects.filter(teacher=user)
        context = {
            'taught_courses': courses.filter(is_active=True),
            'archived_courses': courses.filter(is_active=False),
        }
        return render(request, 'courses/teacher_dashboard.html', context)
    else:
        # For students, show the courses they're enrolled in
        enrollments = Enrollment.objects.filter(student=user, is_active=True)
        courses = Course.objects.filter(enrollment__in=enrollments)
        context = {
            'active_courses': courses.filter(is_active=True),
            'archived_courses': courses.filter(is_active=False),
        }
        return render(request, 'courses/student_dashboard.html', context)

class CourseListView(LoginRequiredMixin, ListView):
    """
    View to list all available courses
    """
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        
        # Search functionality
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset

class CourseDetailView(LoginRequiredMixin, DetailView):
    """
    View to display course details
    """
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        user = self.request.user
        
        # Add enrollment information for students
        if user.is_student():
            try:
                enrollment = Enrollment.objects.get(student=user, course=course)
                context['is_enrolled'] = enrollment.is_active
            except Enrollment.DoesNotExist:
                context['is_enrolled'] = False
        
        # Add sessions
        context['sessions'] = Session.objects.filter(course=course).order_by('date', 'start_time')
        
        return context

class TeacherRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure user is a teacher
    """
    def test_func(self):
        return self.request.user.is_teacher() or self.request.user.is_superuser

class CourseCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    """
    View to create a new course
    """
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:dashboard')
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, _('Course created successfully'))
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    """
    View to update a course
    """
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, _('Course updated successfully'))
        return super().form_valid(form)
    
    def test_func(self):
        course = self.get_object()
        return (self.request.user == course.teacher) or self.request.user.is_superuser

class SessionCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    """
    View to create a new session
    """
    model = Session
    form_class = SessionForm
    template_name = 'courses/session_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        return context
    
    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        form.instance.course = course
        messages.success(self.request, _('Session created successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'pk': self.kwargs.get('course_pk')})
    
    def test_func(self):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        return (self.request.user == course.teacher) or self.request.user.is_superuser

@login_required
def enroll_course(request, course_id):
    """
    Enroll a student in a course
    """
    if not request.user.is_student():
        messages.error(request, _('Only students can enroll in courses'))
        return redirect('courses:course_list')
    
    course = get_object_or_404(Course, pk=course_id)
    
    if not course.is_enrollment_open():
        messages.error(request, _('Enrollment is not open for this course'))
        return redirect('courses:course_detail', pk=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        if enrollment.is_active:
            messages.info(request, _('You are already enrolled in this course'))
        else:
            enrollment.is_active = True
            enrollment.save()
            messages.success(request, _('You have successfully re-enrolled in this course'))
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, _('You have successfully enrolled in this course'))
    
    return redirect('courses:course_detail', pk=course_id)

@login_required
def unenroll_course(request, course_id):
    """
    Unenroll a student from a course
    """
    if not request.user.is_student():
        messages.error(request, _('Only students can unenroll from courses'))
        return redirect('courses:course_list')
    
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    enrollment.is_active = False
    enrollment.save()
    messages.success(request, _('You have successfully unenrolled from this course'))
    
    return redirect('courses:course_detail', pk=course_id)
