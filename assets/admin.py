# assets/admin.py (PHIÊN BẢN HOÀN CHỈNH)

from django.contrib import admin
from .models import ComputerModel, Computer

@admin.register(ComputerModel)
class ComputerModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'cpu', 'ram_gb', 'storage', 'gpu', 'os')
    list_filter = ('brand', 'os')
    search_fields = ('brand', 'model', 'cpu')

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'computer_model', 'serial', 'status', 'current_location', 'assigned_to')
    list_filter = ('status', 'current_location', 'computer_model__brand')
    search_fields = ('asset_tag', 'serial', 'assigned_to__full_name')
    autocomplete_fields = ('computer_model', 'current_location', 'assigned_to', 'assigned_department')