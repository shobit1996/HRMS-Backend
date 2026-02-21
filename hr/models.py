"""
HR App — Database Models.

Employee: stores employee records.
Attendance: stores daily attendance records linked to an Employee.
"""

from django.db import models


class Employee(models.Model):
    """Represents an employee in the system."""

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique employee identifier (e.g. EMP001)",
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.employee_id} — {self.full_name}"


class Attendance(models.Model):
    """Records daily attendance status for a specific employee."""

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Present',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'employee__employee_id']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        # Prevent duplicate attendance for same employee on same day
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.employee_id} — {self.date} — {self.status}"
