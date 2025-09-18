from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Location, InventoryTxn
from .serializers import LocationSerializer, InventoryTxnSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryTxnViewSet(viewsets.ModelViewSet):
    queryset = InventoryTxn.objects.select_related(
        'source_location', 'dest_location', 'created_by', 'received_by'
    ).prefetch_related('lines').all()
    serializer_class = InventoryTxnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='post-transaction')
    def post_transaction(self, request, pk=None):
        instance = self.get_object()

        if instance.status != InventoryTxn.TxnStatus.DRAFT:
            return Response(
                {"error": "Chỉ có thể ghi sổ chứng từ ở trạng thái Nháp."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            instance.process_transaction()
            instance.status = InventoryTxn.TxnStatus.POSTED
            instance.save()
            return Response(
                {"status": "Chứng từ đã được ghi sổ thành công."},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Lỗi không xác định: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)