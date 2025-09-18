from django.contrib import admin
from .models import Position, Department, Employee

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'manager', 'is_active')
    search_fields = ('name', 'code')
    autocomplete_fields = ('manager',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'emp_code', 'position', 'department', 'is_active')
    search_fields = ('full_name', 'emp_code', 'user__username')
    list_filter = ('department', 'position', 'is_active')
    autocomplete_fields = ('user', 'position', 'department')