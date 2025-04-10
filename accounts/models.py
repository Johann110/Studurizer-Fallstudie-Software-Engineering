from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model for Studurizer with additional fields for user roles.
    """
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, _('Student')),
        (TEACHER, _('Teacher')),
        (ADMIN, _('Admin')),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
        help_text=_('Designates the role of this user in the system.')
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text=_('Profile picture of the user')
    )
    
    matriculation_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=_('Student matriculation number')
    )
    
    # Overriding groups and user_permissions to set related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='studurizer_users',
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='studurizer_users',
        help_text=_('Specific permissions for this user.'),
    )
    
    def is_student(self):
        return self.role == self.STUDENT
    
    def is_teacher(self):
        return self.role == self.TEACHER
    
    def is_admin_user(self):
        return self.role == self.ADMIN or self.is_staff
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
