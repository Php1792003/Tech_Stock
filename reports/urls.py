from django.urls import path
from .views import InventoryReportAPIView, RevenueReportAPIView, StockMovementReportAPIView, DashboardStatsAPIView, \
    AssetDepreciationReportAPIView

urlpatterns = [
    path('inventory/', InventoryReportAPIView.as_view(), name='report-inventory'),
    path('revenue/', RevenueReportAPIView.as_view(), name='report-revenue'),
    path('stock-movement/', StockMovementReportAPIView.as_view(), name='report-stock-movement'),
    path('dashboard-stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    path('asset-depreciation/<int:computer_id>/', AssetDepreciationReportAPIView.as_view(), name='asset-depreciation-report'),
]