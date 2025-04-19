from django.urls import path
from events import views

urlpatterns = [
    path('create_event/', views.CreateEvent.as_view(), name='create_event'),
    path('update_event/<int:id>/', views.UpdateEvent.as_view(), name='update_event'),
    path('delete_event/<int:id>/', views.DeleteEvent.as_view(), name='delete_event'),
]