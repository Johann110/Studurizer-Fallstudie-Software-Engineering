from django.urls import path
from grades import views
from grades.views import embedded_pdf_view

urlpatterns = [
    path('create_grade/<int:submission_id>/', views.CreateGradeForSubmission.as_view(), name='create_grade'),
    path('update_grade/<int:submission_id>/<int:pk>/', views.UpdateGradeForSubmission.as_view(), name='update_grade'),
    path('embedded-media/<path:path>', embedded_pdf_view, name='embedded_pdf'), # voll von KI erzeugt
]


