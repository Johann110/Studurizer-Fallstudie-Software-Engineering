from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from events.forms import EventForm
from events.models import Events


class CreateEvent(CreateView):
    model = Events
    template_name = 'events/create_events.html'
    form_class = EventForm
    success_url = reverse_lazy("home")


class UpdateEvent(UpdateView):
    model = Events
    template_name = 'courses/update_course.html'
    form_class = EventForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'pk'


class DeleteEvent(DeleteView):
    model = Events
    success_url = reverse_lazy('home')