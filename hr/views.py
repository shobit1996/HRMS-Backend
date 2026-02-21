"""
HR App — API Views.

Endpoints:
  GET/POST  /api/employees/          — list all employees, create a new one
  DELETE    /api/employees/<id>/     — delete a single employee
  GET/POST  /api/attendance/         — list attendance (with filters), mark attendance
"""

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer


# ─── Employee Views ───────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def employee_list(request):
    """
    GET  — Return list of all employees.
    POST — Create a new employee.
    """
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Build a friendly error message for the React toast
        errors = serializer.errors
        # Collapse nested error lists into a single string
        error_messages = []
        for field, messages in errors.items():
            if isinstance(messages, list):
                error_messages.append(f"{field}: {', '.join(str(m) for m in messages)}")
            else:
                error_messages.append(str(messages))
        return Response(
            {'error': ' | '.join(error_messages)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET', 'DELETE'])
def employee_detail(request, pk):
    """
    GET    — Return a single employee.
    DELETE — Delete a single employee (and their attendance records via CASCADE).
    """
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Attendance Views ─────────────────────────────────────────────────────────

# @api_view(['GET', 'POST', 'PUT'])
# def attendance_list(request):
#     """
#     GET  — Return attendance records.
#            Supports query params:
#              ?employee_id=<pk>          filter by employee primary key
#              ?date_from=YYYY-MM-DD      filter start date (inclusive)
#              ?date_to=YYYY-MM-DD        filter end date (inclusive)

#     POST — Mark attendance for an employee on a date.
#            Body: { employee_ref: <pk>, date: "YYYY-MM-DD", status: "Present"|"Absent" }
#     """
#     if request.method == 'GET':
#         queryset = Attendance.objects.select_related('employee').all()

#         # Apply filters from query params
#         employee_id = request.query_params.get('employee_id')
#         date_from = request.query_params.get('date_from')
#         date_to = request.query_params.get('date_to')

#         if employee_id:
#             queryset = queryset.filter(employee__pk=employee_id)
#         if date_from:
#             queryset = queryset.filter(date__gte=date_from)
#         if date_to:
#             queryset = queryset.filter(date__lte=date_to)

#         serializer = AttendanceSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = AttendanceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # Return a clean error for the React toast
#         errors = serializer.errors
#         if 'error' in errors:
#             # Our custom validate() message
#             return Response({'error': errors['error']}, status=status.HTTP_400_BAD_REQUEST)

#         error_messages = []
#         for field, messages in errors.items():
#             if isinstance(messages, list):
#                 error_messages.append(f"{field}: {', '.join(str(m) for m in messages)}")
#             else:
#                 error_messages.append(str(messages))
#         return Response(
#             {'error': ' | '.join(error_messages)},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

@api_view(['GET', 'POST', 'PUT'])   # ← add PUT here
def attendance_list(request):
    """
    GET   — list attendance records (with filters)
    POST  — create new attendance
    PUT   — update existing attendance
            Body must include: "id": <attendance_pk>, ...
    """
    if request.method == 'GET':
        queryset = Attendance.objects.select_related('employee').all()

        employee_id = request.query_params.get('employee_id')
        date_from    = request.query_params.get('date_from')
        date_to      = request.query_params.get('date_to')

        if employee_id:
            queryset = queryset.filter(employee__pk=employee_id)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method in ['POST', 'PUT']:
        instance = None
        if request.method == 'PUT':
            pk = request.data.get('id')
            if not pk:
                return Response(
                    {'error': 'id is required for update'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                instance = Attendance.objects.get(pk=pk)
            except Attendance.DoesNotExist:
                return Response(
                    {'error': 'Attendance record not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = AttendanceSerializer(
            instance=instance,
            data=request.data,
            partial=True   # ← allows partial updates (very useful)
        )

        if serializer.is_valid():
            serializer.save()
            if request.method == 'POST':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data)   # 200 OK on update

        # Error formatting (same as before)
        errors = serializer.errors
        if 'error' in errors:  # from your custom validate()
            return Response({'error': errors['error']}, status=400)

        error_messages = []
        for field, msgs in errors.items():
            if isinstance(msgs, list):
                error_messages.append(f"{field}: {', '.join(str(m) for m in msgs)}")
            else:
                error_messages.append(str(msgs))

        return Response(
            {'error': ' | '.join(error_messages)},
            status=status.HTTP_400_BAD_REQUEST,
        )
