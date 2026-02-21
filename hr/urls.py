"""
HR App — URL routing.

All routes are prefixed with /api/ from the root urls.py.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Employees
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee-detail'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance-list'),
]
