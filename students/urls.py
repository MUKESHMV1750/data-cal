from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.student_form, name='student_form'),
    path('success/', views.student_success, name='student_success'),
    path('closed/', views.form_closed, name='form_closed'),
]
