from django.urls import path
from courses import views

urlpatterns = [
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('create-course/', views.CreateCourse.as_view(), name='create_course'),
    path('update-course/<int:pk>/', views.UpdateCourse.as_view(), name='update_course'),
    path('delete-course/<int:pk>/', views.DeleteCourse.as_view(), name='delete_course'),
]