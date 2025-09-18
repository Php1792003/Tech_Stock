from rest_framework import serializers
from .models import ComputerModel, Computer
from inventory.models import InventoryTxn
from inventory.serializers import InventoryTxnHistorySerializer


class ComputerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerModel
        fields = '__all__'


class ComputerSerializer(serializers.ModelSerializer):
    computer_model_name = serializers.CharField(source='computer_model.__str__', read_only=True)
    current_location_name = serializers.CharField(source='current_location.name', read_only=True, allow_null=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    history = serializers.SerializerMethodField()

    class Meta:
        model = Computer
        fields = [
            'id', 'asset_tag', 'serial', 'computer_model', 'computer_model_name',
            'purchase_date', 'warranty_expiry', 'purchase_price',
            'status', 'status_display',
            'current_location', 'current_location_name',
            'assigned_to', 'assigned_to_name', 'assigned_department',
            'remark',
            'history'
        ]

    def get_history(self, obj):
        related_txns = InventoryTxn.objects.filter(
            lines__computer=obj
        ).distinct().order_by('posted_at', 'created_at')

        serializer = InventoryTxnHistorySerializer(related_txns, many=True)
        return serializer.data