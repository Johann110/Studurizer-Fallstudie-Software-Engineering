# urls for submissions
from django.urls import path
from submissions import views
urlpatterns = [
    path('create-submission/<int:assignment_id>/', views.create_submission, name='create_submission'),
]