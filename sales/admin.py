from django.contrib import admin

from .models import SalesInvoice, SalesInvoiceLine


class SalesInvoiceLineInline(admin.TabularInline):
    model = SalesInvoiceLine
    extra = 1
    autocomplete_fields = ['computer']

@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer', 'date', 'created_at', 'total_amount', 'created_by')
    list_filter = ('date', 'created_by')
    search_fields = ('invoice_no', 'customer', 'created_by__full_name')
    inlines = [SalesInvoiceLineInline]

