from django.urls import path
from .views import InventoryReportAPIView, RevenueReportAPIView, StockMovementReportAPIView, DashboardStatsAPIView

urlpatterns = [
    path('inventory/', InventoryReportAPIView.as_view(), name='report-inventory'),
    path('revenue/', RevenueReportAPIView.as_view(), name='report-revenue'),
    path('stock-movement/', StockMovementReportAPIView.as_view(), name='report-stock-movement'),

    path('dashboard-stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
]