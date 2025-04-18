from django.shortcuts import render
from django.utils import timezone

from courses.models import Course
from events.models import Events


def home(request):
    events = Events.objects.filter(
        course__students=request.user,  # oder course__teachers=user
        end_time__gt=timezone.now()
    ).order_by('start_time')

    if request.user.groups.filter(name="Teacher").exists():
        taught_courses_qs = Course.objects.filter(teachers=request.user)
        taught_courses = taught_courses_qs.filter(end_date__gte=timezone.now()).order_by('start_date'),
        archived_courses = taught_courses_qs.filter(end_date__lt=timezone.now()).order_by('-end_date'),
        context = {
            'taught_courses': taught_courses,
            'archived_courses': archived_courses,
            'events': events
        }
    else:
        courses = Course.objects.filter(students=request.user)
        active_courses = courses.filter(end_date__gte=timezone.now()).order_by('start_date'),
        archived_courses = courses.filter(end_date__lt=timezone.now()).order_by('-end_date'),
        context = {
            'active_courses': active_courses,
            'archived_courses': archived_courses,
            'events': events
        }
    return render(request, 'homepage.html', context)

def contact(request):
    return render(request,"misc/contact.html")

def imprint(request):
    return render(request,"misc/imprint.html")

def datapolicy(request):
    return render(request,"misc/datapolicy.html")
