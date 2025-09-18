from django.contrib import admin, messages
from .models import Location, InventoryTxn, InventoryTxnLine

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'department')
    list_filter = ('type',)
    search_fields = ('name', 'code')
    autocomplete_fields = ('department',)

class InventoryTxnLineInline(admin.TabularInline):
    model = InventoryTxnLine
    extra = 1
    autocomplete_fields = ('computer',)

@admin.register(InventoryTxn)
class InventoryTxnAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'status', 'dest_location', 'created_by', 'posted_at')
    list_filter = ('type', 'status')
    inlines = [InventoryTxnLineInline]
    actions = ['post_transactions']

    def post_transactions(self, request, queryset):
        for txn in queryset:
            if txn.status == InventoryTxn.TxnStatus.APPROVED:
                txn.status = InventoryTxn.TxnStatus.POSTED
                try:
                    txn.process_transaction()
                    self.message_user(request, f"Đã ghi sổ thành công chứng từ {txn.code}", messages.SUCCESS)
                except ValueError as e:
                    self.message_user(request, f"Lỗi: {e}", messages.ERROR)
            else:
                self.message_user(request, f"Chứng từ {txn.code} chưa được duyệt", messages.WARNING)
    post_transactions.short_description = "Ghi sổ các chứng từ đã duyệt"