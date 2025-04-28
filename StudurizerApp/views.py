from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from courses.models import Course
from events.forms import EventForm
from events.models import Events


def home(request):

    if not request.user.is_authenticated:
        return render(request, 'welcome.html')  # Die neue Willkommensseite

    form = EventForm(user=request.user)
    events = Events.objects.filter(
        Q(course__students=request.user) | Q(course__teachers=request.user),
        end_date__gt=timezone.now()
    ).order_by('start_date').distinct()

    if request.user.groups.filter(name="Teacher").exists():
        taught_courses_qs = Course.objects.filter(teachers=request.user)
        taught_courses = taught_courses_qs.filter(end_date__gte=timezone.now()).order_by('start_date')
        archived_courses = taught_courses_qs.filter(end_date__lt=timezone.now()).order_by('-end_date')
        context = {
            'form': form,
            'taught_courses': taught_courses,
            'archived_courses': archived_courses,
            'events': events
        }
    else:
        courses_qs = Course.objects.filter(students=request.user)
        active_courses = courses_qs.filter(end_date__gte=timezone.now()).order_by('start_date')
        archived_courses = courses_qs.filter(end_date__lt=timezone.now()).order_by('-end_date')
        context = {
            'form': form,
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

def library(request):
    return render(request,"information_services/library.html")

def forum(request):
    return render(request,"information_services/forum.html")

def tools(request):
    return render(request,"information_services/tools.html")

def news(request):
    return render(request,"information_services/news.html")














