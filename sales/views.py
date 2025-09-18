# sales/views.py (PHIÊN BẢN HOÀN CHỈNH)

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from .models import SalesInvoice
from .serializers import SalesInvoiceSerializer
from accounts.models import Employee

class SalesInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SalesInvoice.objects.all().select_related('created_by', 'created_by__department')
    serializer_class = SalesInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            employee = Employee.objects.get(user=self.request.user)
            serializer.save(created_by=employee)
        except Employee.DoesNotExist:
            raise serializers.ValidationError({
                "detail": "Tài khoản của bạn không được liên kết với một hồ sơ nhân viên hợp lệ."
            })