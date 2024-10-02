from django.urls import path
from . import views

urlpatterns = [
    path('add_employee/', views.add_employee, name='add_employee'),
    path('generate_letter/', views.generate_letter, name='generate_letter'),
    path('download_pdf/<str:emp_id>/', views.download_pdf, name='download_pdf'),
]

