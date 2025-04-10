from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('course/<int:course_id>/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('course/<int:course_id>/create/', views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='assignment_update'),
    path('<int:assignment_id>/submit/', views.SubmissionCreateView.as_view(), name='submission_create'),
    path('<int:assignment_id>/update-submission/', views.SubmissionUpdateView.as_view(), name='submission_update'),
    path('submission/<int:submission_id>/download/', views.download_submission, name='download_submission'),
    path('submission/<int:submission_id>/grade/', views.GradeSubmissionView.as_view(), name='grade_submission'),
]
