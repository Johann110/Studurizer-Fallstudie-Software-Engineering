from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Assignment, Submission, Grade

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = ('student', 'submitted_at', 'is_late', 'file_link')
    fields = ('student', 'submitted_at', 'is_late', 'file_link')
    
    def file_link(self, obj):
        """Create a clickable link to the file"""
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        elif obj.text_content:
            return format_html('<span>Text submission</span>')
        return "—"
    file_link.short_description = _('Submission')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_points', 'is_active', 'submission_count')
    list_filter = ('is_active', 'course', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'course__title', 'course__code')
    date_hierarchy = 'due_date'
    filter_horizontal = ('related_documents',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'course', 'created_by')
        }),
        (_('Grading'), {
            'fields': ('max_points',)
        }),
        (_('Schedule'), {
            'fields': ('due_date', 'is_active')
        }),
        (_('Late Submissions'), {
            'fields': ('allow_late_submissions', 'late_penalty_percentage')
        }),
        (_('Related Documents'), {
            'fields': ('related_documents',)
        }),
    )
    
    inlines = [SubmissionInline]
    
    def submission_count(self, obj):
        """Display the number of submissions for the assignment"""
        return obj.submissions.count()
    submission_count.short_description = _('Submissions')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new assignment
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'is_late', 'has_grade')
    list_filter = ('is_late', 'assignment__course', 'submitted_at')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 
                    'assignment__title', 'assignment__course__title')
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at', 'is_late', 'file_preview')
    
    fieldsets = (
        (None, {
            'fields': ('assignment', 'student', 'submitted_at', 'is_late')
        }),
        (_('Submission Content'), {
            'fields': ('file', 'file_preview', 'text_content')
        }),
    )
    
    def file_preview(self, obj):
        """Create a preview or link to the file"""
        if obj.file:
            file_type = obj.file.name.split('.')[-1].lower()
            if file_type in ['jpg', 'jpeg', 'png', 'gif']:
                return format_html('<img src="{}" style="max-width: 300px; max-height: 200px;" />', obj.file.url)
            return format_html('<a href="{}" target="_blank">Download {}</a>', obj.file.url, obj.filename())
        return "—"
    file_preview.short_description = _('File Preview')
    
    def has_grade(self, obj):
        """Check if the submission has been graded"""
        return hasattr(obj, 'grade')
    has_grade.boolean = True
    has_grade.short_description = _('Graded')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('submission_info', 'points', 'percentage', 'graded_by', 'graded_at')
    list_filter = ('graded_at', 'submission__assignment__course')
    search_fields = ('submission__student__username', 'submission__student__first_name', 
                    'submission__student__last_name', 'submission__assignment__title')
    date_hierarchy = 'graded_at'
    
    fieldsets = (
        (None, {
            'fields': ('submission', 'points', 'feedback')
        }),
        (_('Grading Info'), {
            'fields': ('graded_by', 'graded_at')
        }),
    )
    
    readonly_fields = ('graded_at',)
    
    def submission_info(self, obj):
        """Display submission information"""
        return f"{obj.submission.student.username} - {obj.submission.assignment.title}"
    submission_info.short_description = _('Submission')
    
    def percentage(self, obj):
        """Display grade as percentage"""
        percentage = obj.get_percentage()
        return f"{percentage:.1f}%"
    percentage.short_description = _('Percentage')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new grade
            obj.graded_by = request.user
        super().save_model(request, obj, form, change)
