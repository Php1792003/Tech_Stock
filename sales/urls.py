# sales/urls.py (PHIÊN BẢN HOÀN CHỈNH)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesInvoiceViewSet

# 1. Tạo một router
router = DefaultRouter()

# 2. Đăng ký SalesInvoiceViewSet với router
# - 'invoices' là tiền tố URL (ví dụ: /api/sales/invoices/)
# - SalesInvoiceViewSet là viewset xử lý logic
# - basename là tên để tạo các URL name tự động
router.register(r'invoices', SalesInvoiceViewSet, basename='sales-invoice')

# 3. urlpatterns bây giờ sẽ bao gồm tất cả các URL do router tự động tạo ra
urlpatterns = [
    path('', include(router.urls)),
]