from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseForbidden, FileResponse, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from .models import Assignment, Submission, Grade
from courses.models import Course, Enrollment
from .forms import AssignmentForm, SubmissionForm, GradeForm

class CourseTeacherRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure user is the teacher of the specific course or an admin
    """
    def test_func(self):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_id', 0))
        return (self.request.user == course.teacher) or self.request.user.is_admin_user()

class AssignmentListView(LoginRequiredMixin, ListView):
    """
    View to list all assignments for a course
    """
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'
    
    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        
        # Check if user has access to the course
        if not (self.request.user == self.course.teacher or self.request.user.is_admin_user()):
            # Students only see assignments for courses they're enrolled in
            enrollments = Enrollment.objects.filter(
                student=self.request.user,
                course=self.course,
                is_active=True
            )
            if not enrollments.exists():
                return Assignment.objects.none()
        
        # Get assignments and annotate with submission status
        assignments = Assignment.objects.filter(course=self.course)
        
        # Filter by active status if specified
        show_inactive = self.request.GET.get('show_inactive') == 'true'
        if not show_inactive:
            assignments = assignments.filter(is_active=True)
            
        return assignments
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        context['is_teacher'] = (self.request.user == self.course.teacher) or self.request.user.is_admin_user()
        
        # For students, add submission status
        if self.request.user.is_student():
            for assignment in context['assignments']:
                try:
                    submission = Submission.objects.get(
                        assignment=assignment,
                        student=self.request.user
                    )
                    assignment.submission_status = _('Submitted')
                    assignment.submission_date = submission.submitted_at
                    
                    # Check if graded
                    try:
                        grade = Grade.objects.get(submission=submission)
                        assignment.grade_points = grade.points
                        assignment.grade_percentage = grade.get_percentage()
                    except Grade.DoesNotExist:
                        assignment.grade_points = None
                
                except Submission.DoesNotExist:
                    assignment.submission_status = _('Not Submitted')
        
        # For teachers, add submission count
        else:
            for assignment in context['assignments']:
                assignment.submission_count = Submission.objects.filter(assignment=assignment).count()
        
        return context

class AssignmentDetailView(LoginRequiredMixin, DetailView):
    """
    View to display assignment details
    """
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        user = self.request.user
        
        # Add course context
        context['course'] = assignment.course
        
        # Check if user is teacher
        context['is_teacher'] = (user == assignment.course.teacher) or user.is_admin_user()
        
        # For students, add submission info
        if user.is_student():
            try:
                submission = Submission.objects.get(
                    assignment=assignment,
                    student=user
                )
                context['submission'] = submission
                
                # Check if graded
                try:
                    context['grade'] = Grade.objects.get(submission=submission)
                except Grade.DoesNotExist:
                    pass
                
            except Submission.DoesNotExist:
                context['can_submit'] = assignment.can_submit()
        
        # For teachers, add all submissions
        elif context['is_teacher']:
            context['submissions'] = Submission.objects.filter(assignment=assignment).select_related('student', 'grade')
            context['ungraded_count'] = sum(1 for s in context['submissions'] if not hasattr(s, 'grade'))
        
        return context

class AssignmentCreateView(LoginRequiredMixin, CourseTeacherRequiredMixin, CreateView):
    """
    View to create a new assignment
    """
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'])
        context['is_edit'] = False
        return context
    
    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        form.instance.created_by = self.request.user
        messages.success(self.request, _('Assignment created successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('assignments:assignment_detail', kwargs={'pk': self.object.pk})

class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update an assignment
    """
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    
    def test_func(self):
        assignment = self.get_object()
        return (self.request.user == assignment.created_by) or (self.request.user == assignment.course.teacher) or self.request.user.is_admin_user()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course'] = self.object.course
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        context['is_edit'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, _('Assignment updated successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('assignments:assignment_detail', kwargs={'pk': self.object.pk})

class SubmissionCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new submission
    """
    model = Submission
    form_class = SubmissionForm
    template_name = 'assignments/submission_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Get assignment
        self.assignment = get_object_or_404(Assignment, pk=self.kwargs['assignment_id'])
        
        # Check if user is a student
        if not request.user.is_student():
            return HttpResponseForbidden(_("Only students can submit assignments"))
        
        # Check if student is enrolled in the course
        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=self.assignment.course,
            is_active=True
        ).exists()
        
        if not enrollment:
            return HttpResponseForbidden(_("You are not enrolled in this course"))
        
        # Check if assignment allows submissions
        if not self.assignment.can_submit():
            messages.error(request, _("Submissions are no longer being accepted for this assignment"))
            return redirect('assignments:assignment_detail', pk=self.assignment.pk)
        
        # Check if student already has a submission
        existing_submission = Submission.objects.filter(
            assignment=self.assignment,
            student=request.user
        ).exists()
        
        if existing_submission:
            return redirect('assignments:submission_update', 
                           assignment_id=self.assignment.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = self.assignment
        context['course'] = self.assignment.course
        context['is_edit'] = False
        return context
    
    def form_valid(self, form):
        form.instance.assignment = self.assignment
        form.instance.student = self.request.user
        
        # Check if submission is late
        now = timezone.now()
        if now > self.assignment.due_date:
            form.instance.is_late = True
        
        messages.success(self.request, _('Assignment submitted successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('assignments:assignment_detail', kwargs={'pk': self.assignment.pk})

class SubmissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update a submission
    """
    model = Submission
    form_class = SubmissionForm
    template_name = 'assignments/submission_form.html'
    
    def get_object(self):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['assignment_id'])
        return get_object_or_404(Submission, 
                                assignment=assignment, 
                                student=self.request.user)
    
    def test_func(self):
        submission = self.get_object()
        # Only the student who submitted can update
        if self.request.user != submission.student:
            return False
        # Check if assignment still accepts submissions
        return submission.assignment.can_submit()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission = self.get_object()
        context['assignment'] = submission.assignment
        context['course'] = submission.assignment.course
        context['is_edit'] = True
        return context
    
    def form_valid(self, form):
        # Check if submission is late
        submission = self.get_object()
        now = timezone.now()
        if now > submission.assignment.due_date:
            form.instance.is_late = True
        
        messages.success(self.request, _('Submission updated successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('assignments:assignment_detail', kwargs={'pk': self.get_object().assignment.pk})

@login_required
def download_submission(request, submission_id):
    """
    View to download a submission file
    """
    submission = get_object_or_404(Submission, pk=submission_id)
    user = request.user
    
    # Check permissions
    is_teacher = (user == submission.assignment.course.teacher) or user.is_admin_user()
    is_owner = (user == submission.student)
    
    if not (is_teacher or is_owner):
        raise Http404(_("You don't have permission to access this file"))
    
    if not submission.file:
        messages.error(request, _('No file was submitted'))
        return redirect('assignments:assignment_detail', pk=submission.assignment.pk)
    
    try:
        response = FileResponse(submission.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{submission.filename()}"'
        return response
    except:
        messages.error(request, _('Error downloading file'))
        return redirect('assignments:assignment_detail', pk=submission.assignment.pk)

class GradeSubmissionView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View to grade a submission
    """
    model = Grade
    form_class = GradeForm
    template_name = 'assignments/grade_form.html'
    
    def get_submission(self):
        return get_object_or_404(Submission, pk=self.kwargs['submission_id'])
    
    def test_func(self):
        submission = self.get_submission()
        return (self.request.user == submission.assignment.course.teacher) or self.request.user.is_admin_user()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission = self.get_submission()
        context['submission'] = submission
        context['assignment'] = submission.assignment
        context['student'] = submission.student
        context['course'] = submission.assignment.course
        return context
    
    def form_valid(self, form):
        submission = self.get_submission()
        
        # Check if grade already exists
        try:
            existing_grade = Grade.objects.get(submission=submission)
            form.instance = existing_grade
        except Grade.DoesNotExist:
            form.instance.submission = submission
            form.instance.graded_by = self.request.user
        
        messages.success(self.request, _('Submission graded successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        submission = self.get_submission()
        return reverse('assignments:assignment_detail', kwargs={'pk': submission.assignment.pk})
