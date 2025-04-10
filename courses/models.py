from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.models import User

class Course(models.Model):
    """
    Model representing a course in the Studurizer platform
    """
    title = models.CharField(
        max_length=255,
        help_text=_('Course title')
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text=_('Unique course code')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Course description')
    )
    start_date = models.DateField(
        help_text=_('Course start date')
    )
    end_date = models.DateField(
        help_text=_('Course end date')
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether the course is currently active')
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        help_text=_('Course teacher')
    )
    students = models.ManyToManyField(
        User,
        through='Enrollment',
        related_name='enrolled_courses',
        help_text=_('Students enrolled in the course')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    def is_enrollment_open(self):
        """Check if enrollment is currently open for this course"""
        today = timezone.now().date()
        return self.is_active and today <= self.end_date
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = _('course')
        verbose_name_plural = _('courses')


class Enrollment(models.Model):
    """
    Model representing a student's enrollment in a course
    """
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('Enrolled student')
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        help_text=_('Course enrolled in')
    )
    enrollment_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Date of enrollment')
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether the enrollment is active')
    )
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    
    class Meta:
        unique_together = ['student', 'course']
        verbose_name = _('enrollment')
        verbose_name_plural = _('enrollments')


class Session(models.Model):
    """
    Model representing a course session/class
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sessions',
        help_text=_('Course this session belongs to')
    )
    title = models.CharField(
        max_length=255,
        help_text=_('Session title')
    )
    description = models.TextField(
        blank=True,
        help_text=_('Session description')
    )
    date = models.DateField(
        help_text=_('Session date')
    )
    start_time = models.TimeField(
        help_text=_('Session start time')
    )
    end_time = models.TimeField(
        help_text=_('Session end time')
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Session location (if applicable)')
    )
    is_online = models.BooleanField(
        default=False,
        help_text=_('Whether this is an online session')
    )
    online_meeting_link = models.URLField(
        blank=True,
        null=True,
        help_text=_('Link to online meeting (if applicable)')
    )
    
    def __str__(self):
        return f"{self.course.code} - {self.title} ({self.date})"
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = _('session')
        verbose_name_plural = _('sessions')
