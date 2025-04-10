from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'doc_type', 'uploaded_by', 'uploaded_at', 'is_public', 'file_link')
    list_filter = ('doc_type', 'is_public', 'course', 'uploaded_at')
    search_fields = ('title', 'description', 'course__title', 'course__code', 'uploaded_by__username')
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('file_size_display', 'file_type_display', 'uploaded_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file', 'file_size_display', 'file_type_display')
        }),
        (_('Course Information'), {
            'fields': ('course', 'session', 'doc_type')
        }),
        (_('Upload Information'), {
            'fields': ('uploaded_by', 'uploaded_at', 'is_public')
        }),
    )
    
    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.file_size_mb() < 0.1:
            return f"{round(obj.file_size_mb() * 1024, 1)} KB"
        return f"{obj.file_size_mb()} MB"
    file_size_display.short_description = _('File Size')
    
    def file_type_display(self, obj):
        """Display file type based on extension"""
        return obj.file_extension()
    file_type_display.short_description = _('File Type')
    
    def file_link(self, obj):
        """Create a clickable link to the file"""
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
        return "—"
    file_link.short_description = _('File')
