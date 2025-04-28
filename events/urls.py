from django.urls import path
from events import views

urlpatterns = [
    path('create_event/', views.CreateEvent.as_view(), name='create_event'),
    path('create_event/<int:course_id>/', views.CreateEventForCourse.as_view(), name='create_event_for_course'),
    path('delete_event/<int:pk>/', views.DeleteEvent.as_view(), name='delete_event'),
    path('all_events/', views.events, name='all_events'),
]