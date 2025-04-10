from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Course, Enrollment, Session

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    autocomplete_fields = ['student']

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'teacher', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date', 'teacher')
    search_fields = ('title', 'code', 'description', 'teacher__username')
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'code', 'description')
        }),
        (_('Schedule'), {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        (_('Instructor'), {
            'fields': ('teacher',)
        }),
    )
    inlines = [EnrollmentInline, SessionInline]
    autocomplete_fields = ['teacher']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'is_active')
    list_filter = ('is_active', 'enrollment_date', 'course')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'course__title', 'course__code')
    autocomplete_fields = ['student', 'course']
    date_hierarchy = 'enrollment_date'

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'date', 'start_time', 'end_time', 'is_online')
    list_filter = ('is_online', 'date', 'course')
    search_fields = ('title', 'description', 'course__title', 'course__code', 'location')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'description')
        }),
        (_('Schedule'), {
            'fields': ('date', 'start_time', 'end_time')
        }),
        (_('Location'), {
            'fields': ('is_online', 'location', 'online_meeting_link')
        }),
    )
    autocomplete_fields = ['course']
