from django.urls import path
from certificates import views

urlpatterns = [
    path('course/<int:pk>/create-certificates/', views.create_certificate, name='create_certificates'),
]
