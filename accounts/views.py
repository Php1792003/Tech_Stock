from rest_framework import viewsets, permissions
from .models import Position, Department, Employee
from .serializers import PositionSerializer, DepartmentSerializer, EmployeeSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('manager').all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAdminUser]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('user', 'position', 'department').all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]