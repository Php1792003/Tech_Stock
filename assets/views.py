from rest_framework import viewsets, permissions
from .models import ComputerModel, Computer
from .serializers import ComputerModelSerializer, ComputerSerializer

class ComputerModelViewSet(viewsets.ModelViewSet):
    queryset = ComputerModel.objects.all()
    serializer_class = ComputerModelSerializer
    permission_classes = [permissions.IsAdminUser]


class ComputerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.select_related(
        'computer_model', 'current_location', 'assigned_to', 'assigned_department'
    ).prefetch_related(
        'history_lines__inventory_txn__source_location',
        'history_lines__inventory_txn__dest_location',
        'history_lines__inventory_txn__received_by',
        'history_lines__inventory_txn__created_by'
    ).all()

    serializer_class = ComputerSerializer
    permission_classes = [permissions.IsAuthenticated]