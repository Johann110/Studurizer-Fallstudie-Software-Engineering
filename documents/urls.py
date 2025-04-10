from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('course/<int:course_id>/', views.DocumentListView.as_view(), name='document_list'),
    path('course/<int:course_id>/upload/', views.DocumentUploadView.as_view(), name='document_upload'),
    path('download/<int:document_id>/', views.document_download, name='document_download'),
    path('delete/<int:pk>/', views.DocumentDeleteView.as_view(), name='document_delete'),
]
