from django.urls import path
from material import views

urlpatterns = [
    path("delete/<int:materialId>/", views.delete_material, name="delete_material")
]