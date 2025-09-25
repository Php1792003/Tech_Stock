from django.urls import path
from .views import (
    InventoryReportAPIView,
    RevenueReportAPIView,
    StockMovementReportAPIView,
    DashboardStatsAPIView,
    AssetDepreciationReportAPIView,
    AssetAssignmentReportView,
    AssetMaintenanceReportView,
    AssetDisposalReportView,
    AssetUtilizationReportView,
    AssetWarrantyReportView,
    AssetCostAnalysisReportView,
)

urlpatterns = [
    path('inventory/', InventoryReportAPIView.as_view(), name='report-inventory'),
    path('revenue/', RevenueReportAPIView.as_view(), name='report-revenue'),
    path('stock-movement/', StockMovementReportAPIView.as_view(), name='report-stock-movement'),
    path('dashboard-stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    path('asset-depreciation/<int:computer_id>/', AssetDepreciationReportAPIView.as_view(), name='asset-depreciation-report'),
    path("asset-assignment/", AssetAssignmentReportView.as_view(), name="asset-assignment-report"),
    path("asset-maintenance/", AssetMaintenanceReportView.as_view(), name="asset-maintenance-report"),
    path("asset-disposal/", AssetDisposalReportView.as_view(), name="asset-disposal-report"),
    path("asset-utilization/", AssetUtilizationReportView.as_view(), name="asset-utilization-report"),
    path("asset-warranty/", AssetWarrantyReportView.as_view(), name="asset-warranty-report"),
    path("asset-cost-analysis/", AssetCostAnalysisReportView.as_view(), name="asset-cost-analysis-report"),
]
