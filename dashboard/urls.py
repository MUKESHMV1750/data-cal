from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.admin_students, name='admin_students'),
    path('students/<int:pk>/', views.admin_student_detail, name='admin_student_detail'),
    path('students/<int:pk>/edit/', views.admin_student_edit, name='admin_student_edit'),
    path('students/<int:pk>/delete/', views.admin_student_delete, name='admin_student_delete'),
    path('form-control/', views.admin_form_control, name='admin_form_control'),
    path('reports/', views.admin_reports, name='admin_reports'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/excel/', views.export_excel, name='export_excel'),
]
