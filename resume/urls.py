from django.urls import path
from . import views

app_name = 'resume'  # This enables the 'resume:' namespace

urlpatterns = [
    path('form/', views.resume_form_view, name='form'),
    path('preview/', views.resume_preview_view, name='preview'),
    path('download-pdf/', views.download_pdf_view, name='download_pdf'),
]