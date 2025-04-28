from django.urls import path
from assignments import views

urlpatterns = [
    path('create-assignment/<int:course_id>/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('delete-assignment/<int:pk>/', views.DeleteAssignment.as_view(), name='delete_assignment'),
    path('update-assignment/<int:pk>/', views.update_assignment, name='update_assignment'),
    path('delete-file/<int:file_id>/', views.delete_assignment_file, name='delete_assignment_file'),
]
