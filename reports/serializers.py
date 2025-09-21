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