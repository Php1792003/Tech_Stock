from rest_framework import serializers
from .models import Location, InventoryTxn, InventoryTxnLine
from accounts.models import Employee


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class InventoryTxnLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTxnLine
        fields = ['id', 'computer', 'note']


class InventoryTxnSerializer(serializers.ModelSerializer):
    lines = InventoryTxnLineSerializer(many=True, write_only=True)

    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    source_location_name = serializers.CharField(source='source_location.name', read_only=True, allow_null=True)
    dest_location_name = serializers.CharField(source='dest_location.name', read_only=True, allow_null=True)
    received_by_name = serializers.CharField(source='received_by.full_name', read_only=True, allow_null=True)

    class Meta:
        model = InventoryTxn
        fields = [
            'id', 'code', 'type', 'status',
            'source_location', 'source_location_name',
            'dest_location', 'dest_location_name',
            'department', 'received_by', 'received_by_name',
            'created_by', 'created_by_name', 'note', 'posted_at',
            'lines'
        ]
        read_only_fields = ('code', 'status', 'created_by', 'posted_at')

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')

        inventory_txn = InventoryTxn.objects.create(**validated_data)

        for line_data in lines_data:
            InventoryTxnLine.objects.create(inventory_txn=inventory_txn, **line_data)

        return inventory_txn

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['lines'] = InventoryTxnLineSerializer(instance.lines.all(), many=True).data
        return representation


class InventoryTxnHistorySerializer(serializers.ModelSerializer):
    """
    Serializer này chỉ dùng để hiển thị lịch sử của một tài sản.
    Nó được thiết kế để gọn nhẹ và dễ đọc.
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    source_location_name = serializers.CharField(source='source_location.name', read_only=True, allow_null=True)
    dest_location_name = serializers.CharField(source='dest_location.name', read_only=True, allow_null=True)
    received_by_name = serializers.CharField(source='received_by.full_name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = InventoryTxn
        fields = [
            'code',
            'type_display',
            'status_display',
            'posted_at',
            'note',
            'source_location_name',
            'dest_location_name',
            'received_by_name',
            'created_by_name'
        ]