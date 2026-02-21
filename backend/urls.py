"""
Root URL configuration for the HR Management backend.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({'status': 'ok', 'message': 'HR Management API is running'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hr.urls')),
    path('health/', health_check, name='health_check'),
]
