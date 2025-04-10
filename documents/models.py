from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os

from accounts.models import User
from courses.models import Course, Session

def document_upload_path(instance, filename):
    """Generate file path for course documents"""
    # Format: documents/course_id/filename
    return f'documents/course_{instance.course.id}/{filename}'

class Document(models.Model):
    """
    Model for course documents and materials
    """
    DOCUMENT_TYPES = [
        ('lecture', _('Lecture Notes')),
        ('assignment', _('Assignment')),
        ('resource', _('Additional Resource')),
        ('syllabus', _('Syllabus')),
        ('other', _('Other')),
    ]
    
    title = models.CharField(
        max_length=255,
        help_text=_('Document title')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Document description')
    )
    file = models.FileField(
        upload_to=document_upload_path,
        help_text=_('The document file'),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'zip', 'png', 'jpg', 'jpeg', 'gif']
            )
        ]
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text=_('Course this document belongs to')
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.SET_NULL,
        related_name='documents',
        null=True,
        blank=True,
        help_text=_('Session this document is related to (if applicable)')
    )
    doc_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        default='resource',
        help_text=_('Type of document')
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_documents',
        help_text=_('User who uploaded this document')
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Date and time of upload')
    )
    is_public = models.BooleanField(
        default=True,
        help_text=_('Whether the document is visible to all course participants')
    )
    
    def __str__(self):
        return self.title
    
    def filename(self):
        """Return just the filename of the document"""
        return os.path.basename(self.file.name)
    
    def file_extension(self):
        """Return the file extension"""
        _, extension = os.path.splitext(self.file.name)
        return extension.lower()
    
    def file_size_mb(self):
        """Return file size in MB"""
        try:
            size_bytes = self.file.size
            return round(size_bytes / (1024 * 1024), 2)
        except:
            return 0
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = _('document')
        verbose_name_plural = _('documents')
