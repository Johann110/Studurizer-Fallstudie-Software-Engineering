from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<int:course_pk>/session/create/', views.SessionCreateView.as_view(), name='session_create'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
]
