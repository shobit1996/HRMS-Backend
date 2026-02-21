"""
HR App — Django Admin registration.
"""

from django.contrib import admin
from .models import Employee, Attendance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'created_at']
    list_filter = ['department']
    search_fields = ['employee_id', 'full_name', 'email']
    ordering = ['employee_id']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['get_employee_id', 'get_employee_name', 'date', 'status']
    list_filter = ['status', 'date', 'employee__department']
    search_fields = ['employee__employee_id', 'employee__full_name']
    ordering = ['-date']
    date_hierarchy = 'date'

    @admin.display(description='Employee ID', ordering='employee__employee_id')
    def get_employee_id(self, obj):
        return obj.employee.employee_id

    @admin.display(description='Employee Name', ordering='employee__full_name')
    def get_employee_name(self, obj):
        return obj.employee.full_name
