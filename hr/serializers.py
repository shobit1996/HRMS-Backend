"""
HR App — Serializers.

Converts Django model instances to/from JSON for the REST API.
"""

from rest_framework import serializers
from .models import Employee, Attendance


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model — full CRUD."""

    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_employee_id(self, value):
        """Ensure employee_id is stripped and non-empty."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Employee ID cannot be blank.")
        return value

    def validate_email(self, value):
        """Ensure email is lowercase."""
        return value.lower().strip()


# class AttendanceSerializer(serializers.ModelSerializer):
#     """
#     Serializer for Attendance model.

#     On read: include denormalized employee_id and employee_name so the
#     React table can display them without a separate API call.
#     On write: accept employee_ref (the Employee primary key) as sent by
#     the React form.
#     """

#     # Read-only display fields pulled from the related Employee
#     employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
#     employee_name = serializers.CharField(source='employee.full_name', read_only=True)
#     employee_pk    = serializers.IntegerField(source='employee.id', read_only=True)   # ← add this

#     # Write-only field matching what the React form sends (employee_ref = pk)
#     employee_ref = serializers.PrimaryKeyRelatedField(
#         queryset=Employee.objects.all(),
#         source='employee',        # maps employee_ref → employee FK
#         write_only=True,
#     )

#     class Meta:
#         model = Attendance
#         fields = [
#             'id',
#             'employee_ref',    # write
#             'employee_id',     # read
#             'employee_name',   # read
#             'date',
#             'status',
#             'created_at',
#         ]
#         read_only_fields = ['id', 'employee_id', 'employee_name', 'employee_pk' 'created_at']

#     def validate(self, data):
#         """
#         Prevent duplicate attendance entry for the same employee on the same date.
#         Raise a clear error message so the React toast can display it.
#         """
#         employee = data.get('employee')
#         date = data.get('date')

#         if employee and date:
#             qs = Attendance.objects.filter(employee=employee, date=date)
#             # Exclude current instance when updating
#             if self.instance:
#                 qs = qs.exclude(pk=self.instance.pk)
#             if qs.exists():
#                 raise serializers.ValidationError({
#                     'error': f"Attendance for {employee.full_name} on {date} is already marked."
#                 })
#         return data

class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model.

    On read: include denormalized employee_id, employee_name, employee_pk
    On write: accept employee_ref (the Employee primary key)
    """

    # Read-only display fields pulled from the related Employee
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_pk = serializers.IntegerField(source='employee.id', read_only=True)  # ← added

    # Write-only field for incoming data from React
    employee_ref = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',        # maps employee_ref → Attendance.employee FK
        write_only=True,
    )

    class Meta:
        model = Attendance
        fields = [
            'id',
            'employee_ref',     # write-only
            'employee_id',      # read-only
            'employee_name',    # read-only
            'employee_pk',      # ← ADD THIS LINE
            'date',
            'status',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'employee_id',
            'employee_name',
            'employee_pk',      # ← also add here
            'created_at',
        ]

    def validate(self, data):
        """
        Prevent duplicate attendance entry for the same employee on the same date.
        """
        employee = data.get('employee')
        date = data.get('date')

        if employee and date:
            qs = Attendance.objects.filter(employee=employee, date=date)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'error': f"Attendance for {employee.full_name} on {date} is already marked."
                })
        return data
