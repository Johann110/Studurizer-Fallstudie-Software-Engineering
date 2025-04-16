from django.shortcuts import render
from django.utils import timezone


def home(request):
    events = Event.objects.filter(
        course__students=request.user,  # oder course__teachers=user
        end_time__gt=timezone.now()
    ).order_by('start_time')
    context = {
        'events': events
    }
    return render(request, 'homepage.html', context)
