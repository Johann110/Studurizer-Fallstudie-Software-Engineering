from django.urls import path
from assignments import views

urlpatterns = [
    path('create-assignment/<int:course_id>/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
]
