from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils import timezone

from courses.models import Course
from events.forms import EventForm
from events.models import Events


class CreateEvent(CreateView):
    model = Events
    form_class = EventForm
    success_url = reverse_lazy("home")


class DeleteEvent(View):
    def post(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        event.delete()
        return redirect('all_events')



def events(request):
    user_courses_q = Q(course__students=request.user) | Q(course__teachers=request.user)
    now = timezone.now()
    events = Events.objects.filter(
        user_courses_q,
        end_date__gte=now
    ).order_by('start_date').select_related('course').distinct()
    archived_main_events = Events.objects.filter(
        user_courses_q,
        end_date__lte=now
    ).order_by('end_date').select_related('course').distinct()
    archived_misc_events = Events.objects.filter(
        course=None,
        end_date__lte=now
    ).order_by('end_date').distinct()
    expired_events = archived_main_events | archived_misc_events
    misc_events =Events.objects.filter(
        course=None,
        end_date__gte=now
    ).order_by('start_date').distinct()
    context = {
        'events': events,
        'expired_events': expired_events,
        'misc_events': misc_events
    }
    return render(request, 'events/eventsdetail.html',context)