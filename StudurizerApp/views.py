from django.shortcuts import render
from django.utils import timezone


def home(request):
    #events = Event.objects.filter(
    #    course__students=request.user,  # oder course__teachers=user
    #    end_time__gt=timezone.now()
    #).order_by('start_time')
    #context = {
    #    'events': events
    #}
    #return render(request, 'homepage.html', context)
    return render(request, 'homepage.html')

def contact(request):
    return render(request,"misc/contact.html")

def imprint(request):
    return render(request,"misc/imprint.html")

def datapolicy(request):
    return render(request,"misc/datapolicy.html")
