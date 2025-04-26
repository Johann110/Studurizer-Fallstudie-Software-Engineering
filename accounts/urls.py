from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

from accounts.forms import CustomUserAuthenticationForm
from accounts.views import profile_detail, profile_edit, profile_delete_picture
urlpatterns = [
    path('login/', views.LoginView.as_view(template_name="accounts/login.html", form_class=CustomUserAuthenticationForm), name='login'),
    path('profile/<int:id>/', profile_detail, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/delete-picture/', profile_delete_picture, name='profile_delete_picture'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)