"""
URL configuration for StudurizerApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from StudurizerApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('news/', news, name='news'),
    path('tools/', tools, name='tools'),
    path('library/', library, name='library'),
    path('forum/', forum, name='forum'),
    path('datapolicy/', datapolicy, name='datapolicy'),
    path('imprint/', imprint, name='imprint'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('events/', include('events.urls')),
    path('material/', include('material.urls')),
    path('assignments/', include('assignments.urls')),
    path('submissions/', include('submissions.urls')),
    path('grades/', include('grades.urls')),
    path('certificates/', include('certificates.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
