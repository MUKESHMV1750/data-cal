"""
URL configuration for student_data_collection project.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from students import views as index_views

urlpatterns = [
    path('', index_views.index, name='index'),
    path('student/', include('students.urls')),
    path('admin/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
