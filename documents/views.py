from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Document
from courses.models import Course
from .forms import DocumentUploadForm

class TeacherRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure user is a teacher or admin
    """
    def test_func(self):
        return self.request.user.is_teacher() or self.request.user.is_admin_user()

class CourseTeacherRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure user is the teacher of the specific course or an admin
    """
    def test_func(self):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_id', 0))
        return (self.request.user == course.teacher) or self.request.user.is_admin_user()

class DocumentListView(LoginRequiredMixin, ListView):
    """
    View to list documents for a specific course
    """
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    
    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        
        # Check if user has access to the course
        if not (self.request.user.is_teacher() or self.request.user.is_admin_user()):
            # Students only see documents for courses they're enrolled in
            enrollments = self.request.user.enrollment_set.filter(
                course=self.course, 
                is_active=True
            )
            if not enrollments.exists():
                return Document.objects.none()
        
        # Filter by document type if specified
        doc_type = self.request.GET.get('type')
        queryset = Document.objects.filter(course=self.course)
        
        if doc_type:
            queryset = queryset.filter(doc_type=doc_type)
        
        # Students only see public documents
        if not (self.request.user.is_teacher() or self.request.user.is_admin_user() or 
                self.request.user == self.course.teacher):
            queryset = queryset.filter(is_public=True)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        context['document_types'] = Document.DOCUMENT_TYPES
        context['current_type'] = self.request.GET.get('type', '')
        context['can_upload'] = (self.request.user == self.course.teacher) or self.request.user.is_admin_user()
        return context

class DocumentUploadView(LoginRequiredMixin, CourseTeacherRequiredMixin, CreateView):
    """
    View to upload a new document
    """
    model = Document
    form_class = DocumentUploadForm
    template_name = 'documents/document_upload.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return context
    
    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, _('Document uploaded successfully'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('documents:document_list', kwargs={'course_id': self.kwargs['course_id']})

class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete a document
    """
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    context_object_name = 'document'
    
    def test_func(self):
        document = self.get_object()
        return (self.request.user == document.uploaded_by) or (self.request.user == document.course.teacher) or self.request.user.is_admin_user()
    
    def get_success_url(self):
        messages.success(self.request, _('Document deleted successfully'))
        return reverse_lazy('documents:document_list', kwargs={'course_id': self.object.course.id})

@login_required
def document_download(request, document_id):
    """
    View to download a document
    """
    document = get_object_or_404(Document, pk=document_id)
    course = document.course
    
    # Check if user has access to the document
    is_course_teacher = request.user == course.teacher
    is_admin = request.user.is_admin_user()
    
    if not (is_course_teacher or is_admin):
        # Check if student is enrolled in the course
        enrolled = request.user.enrollment_set.filter(course=course, is_active=True).exists()
        
        if not enrolled or (not document.is_public and not is_course_teacher and not is_admin):
            raise Http404(_("You don't have permission to access this document"))
    
    try:
        response = FileResponse(document.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{document.filename()}"'
        return response
    except:
        messages.error(request, _('Error downloading file'))
        return redirect('documents:document_list', course_id=course.id)
