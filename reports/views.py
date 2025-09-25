# reports/views.py (PHIÊN BẢN HOÀN CHỈNH)
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count, Q, F, Sum, Case, When, IntegerField
from django.db.models.functions import TruncMonth
from datetime import datetime, date
from collections import defaultdict
from django.utils import timezone

from assets.models import Computer, ComputerModel
from sales.models import SalesInvoiceLine, SalesInvoice
from inventory.models import Location, InventoryTxnLine

from .serializers import InventoryReportSerializer, RevenueReportSerializer, StockMovementReportSerializer, \
    DepreciationScheduleEntrySerializer


class InventoryReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Computer.objects.exclude(status=Computer.StatusChoices.DISPOSED) \
            .values('current_location__name', 'computer_model__brand', 'computer_model__model') \
            .annotate(
                quantity=Count('id'),
                total_value=Sum('purchase_price')
            ).order_by('current_location__name', 'computer_model__brand')

        serializer = InventoryReportSerializer(queryset, many=True)
        return Response(serializer.data)


class RevenueReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = SalesInvoiceLine.objects \
            .annotate(period=TruncMonth('invoice__date')) \
            .values('period') \
            .annotate(
                total_revenue=Sum('total_price'),
                total_cogs=Sum('cost_allocated')
            ).annotate(
                gross_profit=F('total_revenue') - F('total_cogs')
            ).order_by('period')

        serializer = RevenueReportSerializer(queryset, many=True)
        return Response(serializer.data)


class StockMovementReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        try:
            today = date.today()
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else today.replace(day=1)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else today
        except ValueError:
            return Response({"error": "Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        stock_in_movements = InventoryTxnLine.objects.filter(
            inventory_txn__dest_location__isnull=False, inventory_txn__posted_at__date__lte=end_date
        ).values('inventory_txn__dest_location', 'computer__computer_model').annotate(
            opening_stock=Count(Case(When(inventory_txn__posted_at__lt=start_date, then=1), output_field=IntegerField())),
            stock_in=Count(Case(When(inventory_txn__posted_at__date__range=(start_date, end_date), then=1), output_field=IntegerField()))
        )

        stock_out_movements = InventoryTxnLine.objects.filter(
            inventory_txn__source_location__isnull=False, inventory_txn__posted_at__date__lte=end_date
        ).values('inventory_txn__source_location', 'computer__computer_model').annotate(
            opening_stock=Count(Case(When(inventory_txn__posted_at__lt=start_date, then=1), output_field=IntegerField())),
            stock_out=Count(Case(When(inventory_txn__posted_at__date__range=(start_date, end_date), then=1), output_field=IntegerField()))
        )

        report_data_dict = defaultdict(lambda: {'opening_stock': 0, 'stock_in': 0, 'stock_out': 0})

        for item in stock_in_movements:
            key = (item['inventory_txn__dest_location'], item['computer__computer_model'])
            report_data_dict[key]['opening_stock'] += item['opening_stock']
            report_data_dict[key]['stock_in'] += item['stock_in']

        for item in stock_out_movements:
            key = (item['inventory_txn__source_location'], item['computer__computer_model'])
            report_data_dict[key]['opening_stock'] -= item['opening_stock']
            report_data_dict[key]['stock_out'] += item['stock_out']

        final_report = []
        locations = {loc.id: loc for loc in Location.objects.all()}
        computer_models = {cm.id: cm for cm in ComputerModel.objects.all()}

        for (location_id, model_id), data in report_data_dict.items():
            opening_stock = data['opening_stock']
            stock_in = data['stock_in']
            stock_out = data['stock_out']
            closing_stock = opening_stock + stock_in - stock_out

            if opening_stock != 0 or stock_in != 0 or stock_out != 0:
                location = locations.get(location_id)
                model = computer_models.get(model_id)
                if location and model:
                    final_report.append({
                        'location_id': location.id,
                        'location_name': location.name,
                        'computer_model_id': model.id,
                        'computer_model_name': str(model),
                        'opening_stock': opening_stock,
                        'stock_in': stock_in,
                        'stock_out': stock_out,
                        'closing_stock': closing_stock,
                    })

        final_report.sort(key=lambda x: (x['location_name'], x['computer_model_name']))
        serializer = StockMovementReportSerializer(final_report, many=True)
        return Response(serializer.data)


class DashboardStatsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_assets = Computer.objects.count()
        total_asset_value = Computer.objects.aggregate(total_value=Sum('purchase_price'))['total_value'] or 0

        asset_status_summary = list(
            Computer.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        status_display_map = dict(Computer.StatusChoices.choices)
        for item in asset_status_summary:
            item['status_display'] = status_display_map.get(item['status'], item['status'])

        current_month = timezone.now().month
        current_year = timezone.now().year

        current_month_revenue = SalesInvoice.objects.filter(
            date__year=current_year,
            date__month=current_month
        ).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0

        data = {
            'total_assets': total_assets,
            'total_asset_value': total_asset_value,
            'asset_status_summary': asset_status_summary,
            'current_month_revenue': current_month_revenue,
        }

        return Response(data, status=status.HTTP_200_OK)


class AssetDepreciationReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, computer_id, *args, **kwargs):
        try:
            computer = Computer.objects.get(pk=computer_id)
        except Computer.DoesNotExist:
            return Response({"error": "Tài sản không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        if not computer.purchase_date or computer.useful_life <= 0:
            return Response({
                "error": "Tài sản thiếu thông tin Ngày mua hoặc Vòng đời sử dụng để tính khấu hao."
            }, status=status.HTTP_400_BAD_REQUEST)

        original_cost = computer.purchase_price
        salvage_value = computer.salvage_value
        useful_life_months = computer.useful_life * 12

        depreciable_base = original_cost - salvage_value
        if depreciable_base < 0: depreciable_base = 0

        monthly_depreciation = depreciable_base / useful_life_months

        schedule = []
        accumulated_depreciation = 0
        current_date = computer.purchase_date

        for month in range(1, useful_life_months + 1):
            accumulated_depreciation += monthly_depreciation

            if accumulated_depreciation > depreciable_base:
                accumulated_depreciation = depreciable_base

            book_value = original_cost - accumulated_depreciation

            schedule.append({
                "period_date": current_date,
                "monthly_depreciation": monthly_depreciation,
                "accumulated_depreciation": round(accumulated_depreciation, 0),
                "book_value": round(book_value, 0)
            })

            current_date += relativedelta(months=1)

        schedule_serializer = DepreciationScheduleEntrySerializer(schedule, many=True)

        data = {
            "asset_info": {
                "id": computer.id,
                "asset_tag": computer.asset_tag,
                "name": str(computer.computer_model),
            },
            "depreciation_summary": {
                "original_cost": original_cost,
                "salvage_value": salvage_value,
                "depreciable_base": depreciable_base,
                "useful_life_years": computer.useful_life,
                "monthly_depreciation": round(monthly_depreciation, 0),
            },
            "schedule": schedule_serializer.data
        }
class AssetAssignmentReportView(APIView):
    def get(self, request):
        data = [
            {
                "employee_id": 101,
                "employee_name": "Nguyen Van A",
                "department": "IT",
                "assigned_assets": [
                    {
                        "computer_id": 5,
                        "asset_tag": "APPLE-MBP-001",
                        "model": "Apple Macbook Pro 14 M3",
                        "assigned_date": "2025-09-10",
                        "status": "IN_USE"
                    }
                ]
            },
            {
                "employee_id": 102,
                "employee_name": "Tran Thi B",
                "department": "Finance",
                "assigned_assets": [
                    {
                        "computer_id": 8,
                        "asset_tag": "DELL-LAT-002",
                        "model": "Dell Latitude 7440",
                        "assigned_date": "2025-08-25",
                        "status": "IN_USE"
                    }
                ]
            }
        ]
        return Response(data)

class AssetMaintenanceReportView(APIView):
    def get(self, request):
        data = [
            {
                "computer_id": 12,
                "asset_tag": "HP-ELITE-001",
                "model": "HP EliteBook 840 G9",
                "last_maintenance_date": "2025-08-15",
                "next_maintenance_date": "2026-02-15",
                "maintenance_history": [
                    {
                        "date": "2025-02-15",
                        "type": "SCHEDULED",
                        "description": "Bảo trì định kỳ 6 tháng",
                        "cost": "500000"
                    },
                    {
                        "date": "2025-08-15",
                        "type": "REPAIR",
                        "description": "Thay pin laptop",
                        "cost": "1800000"
                    }
                ],
                "total_maintenance_cost": "2300000",
                "status": "IN_USE"
            }
        ]
        return Response(data)

class AssetDisposalReportView(APIView):
    def get(self, request):
        data = [
            {
                "computer_id": 20,
                "asset_tag": "LENOVO-THINK-001",
                "model": "Lenovo ThinkPad X1 Carbon Gen10",
                "purchase_date": "2022-01-15",
                "disposal_date": "2025-09-01",
                "original_cost": "32000000",
                "accumulated_depreciation": "24000000",
                "book_value": "8000000",
                "disposal_value": "7000000",
                "loss_gain": "-1000000",
                "disposal_method": "SALE",
                "buyer": "Công ty ABC"
            }
        ]
        return Response(data)

class AssetUtilizationReportView(APIView):
    def get(self, request):
        data = [
            {
                "computer_id": 30,
                "asset_tag": "DELL-OPT-001",
                "model": "Dell OptiPlex 7090",
                "assigned_to": "Nguyen Van A",
                "department": "IT",
                "utilization_rate": "85%",
                "active_hours": 1700,
                "idle_hours": 300,
                "period": "2025-Q3",
                "status": "IN_USE"
            }
        ]
        return Response(data)

class AssetWarrantyReportView(APIView):
    def get(self, request):
        data = [
            {
                "computer_id": 40,
                "asset_tag": "MSI-GS66-001",
                "model": "MSI GS66 Stealth",
                "purchase_date": "2024-05-01",
                "warranty_period_months": 24,
                "warranty_expiry_date": "2026-05-01",
                "vendor": "MSI Vietnam",
                "support_contact": "support@msi.com",
                "status": "VALID"
            }
        ]
        return Response(data)

class AssetCostAnalysisReportView(APIView):
    def get(self, request):
        data = [
            {
                "computer_id": 50,
                "asset_tag": "HP-PRO-001",
                "model": "HP ProBook 450 G9",
                "purchase_date": "2023-03-15",
                "original_cost": "25000000",
                "maintenance_costs": "3000000",
                "repair_costs": "1500000",
                "depreciation_value": "8000000",
                "disposal_value": "5000000",
                "total_cost_of_ownership": "31500000",
                "current_status": "IN_USE"
            }
        ]
        return Response(data)