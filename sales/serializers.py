from rest_framework import serializers
from .models import SalesInvoice, SalesInvoiceLine


class SalesInvoiceLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesInvoiceLine
        fields = [
            'id',
            'computer',
            'quantity',
            'unit_price',
            'total_price',
            'cost_allocated'
        ]
        read_only_fields = ('total_price', 'cost_allocated')


class SalesInvoiceSerializer(serializers.ModelSerializer):
    lines = SalesInvoiceLineSerializer(many=True, write_only=True)

    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    department_name = serializers.CharField(source='created_by.department.name', read_only=True, allow_null=True)

    class Meta:
        model = SalesInvoice
        fields = [
            'id',
            'invoice_no',
            'customer',
            'date',
            'created_at',
            'total_amount',
            'created_by',
            'created_by_name',
            'department_name',
            'lines'
        ]

        read_only_fields = (
            'total_amount',
            'created_by',
            'created_at',
            'created_by_name',
            'department_name'
        )

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')

        invoice = SalesInvoice.objects.create(**validated_data)

        total_amount = 0
        for line_data in lines_data:
            line = SalesInvoiceLine.objects.create(invoice=invoice, **line_data)
            total_amount += line.total_price

        invoice.total_amount = total_amount
        invoice.save()

        return invoice

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        lines = SalesInvoiceLine.objects.filter(invoice=instance)
        representation['lines'] = SalesInvoiceLineSerializer(lines, many=True).data

        return representation