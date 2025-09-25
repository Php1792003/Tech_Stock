from rest_framework import serializers

class InventoryReportSerializer(serializers.Serializer):
    current_location_name = serializers.CharField(source='current_location__name')
    computer_model_brand = serializers.CharField(source='computer_model__brand')
    computer_model_model = serializers.CharField(source='computer_model__model')
    quantity = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=18, decimal_places=0)

class RevenueReportSerializer(serializers.Serializer):
    period = serializers.DateField()

    total_revenue = serializers.DecimalField(max_digits=18, decimal_places=0)
    total_cogs = serializers.DecimalField(max_digits=18, decimal_places=0)
    gross_profit = serializers.DecimalField(max_digits=18, decimal_places=0)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['period'] = instance['period'].strftime('%Y-%m')
        return representation

class StockMovementReportSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    location_name = serializers.CharField()
    computer_model_id = serializers.IntegerField()
    computer_model_name = serializers.CharField()
    opening_stock = serializers.IntegerField()
    stock_in = serializers.IntegerField()
    stock_out = serializers.IntegerField()
    closing_stock = serializers.IntegerField()

class DepreciationScheduleEntrySerializer(serializers.Serializer):
    period_date = serializers.DateField()
    monthly_depreciation = serializers.DecimalField(max_digits=18, decimal_places=0)
    accumulated_depreciation = serializers.DecimalField(max_digits=18, decimal_places=0)
    book_value = serializers.DecimalField(max_digits=18, decimal_places=0)

class AssetAssignmentReportSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    department = serializers.CharField()
    assigned_assets = serializers.ListField()

class AssetMaintenanceReportSerializer(serializers.Serializer):
    computer_id = serializers.IntegerField()
    asset_tag = serializers.CharField()
    model = serializers.CharField()
    last_maintenance_date = serializers.DateField()
    next_maintenance_date = serializers.DateField()
    maintenance_history = serializers.ListField()
    total_maintenance_cost = serializers.CharField()
    status = serializers.CharField()

class AssetDisposalReportSerializer(serializers.Serializer):
    computer_id = serializers.IntegerField()
    asset_tag = serializers.CharField()
    model = serializers.CharField()
    purchase_date = serializers.DateField()
    disposal_date = serializers.DateField()
    original_cost = serializers.CharField()
    accumulated_depreciation = serializers.CharField()
    book_value = serializers.CharField()
    disposal_value = serializers.CharField()
    loss_gain = serializers.CharField()
    disposal_method = serializers.CharField()
    buyer = serializers.CharField()

class AssetUtilizationReportSerializer(serializers.Serializer):
    computer_id = serializers.IntegerField()
    asset_tag = serializers.CharField()
    model = serializers.CharField()
    assigned_to = serializers.CharField()
    department = serializers.CharField()
    utilization_rate = serializers.CharField()
    active_hours = serializers.IntegerField()
    idle_hours = serializers.IntegerField()
    period = serializers.CharField()
    status = serializers.CharField()

class AssetWarrantyReportSerializer(serializers.Serializer):
    computer_id = serializers.IntegerField()
    asset_tag = serializers.CharField()
    model = serializers.CharField()
    purchase_date = serializers.DateField()
    warranty_period_months = serializers.IntegerField()
    warranty_expiry_date = serializers.DateField()
    vendor = serializers.CharField()
    support_contact = serializers.CharField()
    status = serializers.CharField()

class AssetCostAnalysisReportSerializer(serializers.Serializer):
    computer_id = serializers.IntegerField()
    asset_tag = serializers.CharField()
    model = serializers.CharField()
    purchase_date = serializers.DateField()
    original_cost = serializers.CharField()
    maintenance_costs = serializers.CharField()
    repair_costs = serializers.CharField()
    depreciation_value = serializers.CharField()
    disposal_value = serializers.CharField()
    total_cost_of_ownership = serializers.CharField()
    current_status = serializers.CharField()