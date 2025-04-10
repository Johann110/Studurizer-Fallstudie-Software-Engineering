from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
import os

from accounts.models import User
from courses.models import Course
from documents.models import Document

def submission_upload_path(instance, filename):
    """Generate file path for assignment submissions"""
    # Format: submissions/course_id/assignment_id/user_id/filename
    return f'submissions/course_{instance.assignment.course.id}/assignment_{instance.assignment.id}/user_{instance.student.id}/{filename}'

class Assignment(models.Model):
    """
    Model representing an assignment in a course
    """
    title = models.CharField(
        max_length=255,
        help_text=_('Assignment title')
    )
    description = models.TextField(
        help_text=_('Assignment instructions')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments',
        help_text=_('Course this assignment belongs to')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_assignments',
        help_text=_('Teacher who created the assignment')
    )
    max_points = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text=_('Maximum points possible for this assignment')
    )
    due_date = models.DateTimeField(
        help_text=_('Assignment due date and time')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether the assignment is currently active')
    )
    allow_late_submissions = models.BooleanField(
        default=False,
        help_text=_('Allow submissions after the due date')
    )
    late_penalty_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        help_text=_('Percentage deduction for late submissions (0-100)')
    )
    related_documents = models.ManyToManyField(
        Document,
        related_name='related_assignments',
        blank=True,
        help_text=_('Documents related to this assignment')
    )
    
    def __str__(self):
        return f"{self.title} ({self.course.code})"
    
    def is_past_due(self):
        """Check if the assignment due date has passed"""
        return timezone.now() > self.due_date
    
    def can_submit(self):
        """Check if submissions are still allowed"""
        if not self.is_active:
            return False
        
        is_past_due = self.is_past_due()
        return not is_past_due or (is_past_due and self.allow_late_submissions)
    
    def get_formatted_max_points(self):
        """Return the max points formatted according to its value"""
        if self.max_points % 10 == 0:
            return int(self.max_points / 10)
        return self.max_points / 10
    
    class Meta:
        ordering = ['-due_date']
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')


class Submission(models.Model):
    """
    Model representing a student's submission for an assignment
    """
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=_('Assignment this submission is for')
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=_('Student who submitted')
    )
    file = models.FileField(
        upload_to=submission_upload_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'txt']
            )
        ],
        help_text=_('Submitted file (if applicable)')
    )
    text_content = models.TextField(
        blank=True,
        help_text=_('Text submission content (if applicable)')
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Date and time of submission')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('Date and time of last update')
    )
    is_late = models.BooleanField(
        default=False,
        help_text=_('Whether this submission was submitted after the due date')
    )
    
    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"
    
    def filename(self):
        """Return just the filename of the submission file"""
        if self.file:
            return os.path.basename(self.file.name)
        return None
    
    def file_size_mb(self):
        """Return file size in MB"""
        if self.file:
            try:
                size_bytes = self.file.size
                return round(size_bytes / (1024 * 1024), 2)
            except:
                pass
        return 0
    
    class Meta:
        unique_together = ['assignment', 'student']
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')


class Grade(models.Model):
    """
    Model representing the grade for a submission
    """
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade',
        help_text=_('Submission being graded')
    )
    points = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Points awarded')
    )
    feedback = models.TextField(
        blank=True,
        help_text=_('Feedback for the student')
    )
    graded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grades_given',
        help_text=_('Teacher who graded this submission')
    )
    graded_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Date and time of grading')
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    def __str__(self):
        return f"Grade for {self.submission}"
    
    def get_percentage(self):
        """Calculate the percentage score"""
        max_points = self.submission.assignment.max_points
        if max_points > 0:
            return (self.points / max_points) * 100
        return 0
    
    class Meta:
        verbose_name = _('grade')
        verbose_name_plural = _('grades')
