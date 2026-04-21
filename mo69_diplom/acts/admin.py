"""
Админ-панель для приложения актов КС-2/КС-3.
"""

from django.contrib import admin
from .models import Contractor, Object, WorkType, Contract, Act, ActItem


class ActItemInline(admin.TabularInline):
    """
    Inline отображение строк акта в админке.
    """
    model = ActItem
    extra = 1
    fields = ['number', 'name', 'unit', 'quantity', 'price', 'total']
    readonly_fields = ['total']


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    """
    Админка для контрагентов.
    """
    list_display = ['name', 'inn', 'kpp', 'phone', 'email']
    search_fields = ['name', 'inn', 'kpp', 'email']
    ordering = ['name']


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    """
    Админка для объектов строительства.
    """
    list_display = ['name', 'code', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code', 'address']
    ordering = ['name']


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    """
    Админка для видов работ.
    """
    list_display = ['name', 'code', 'unit']
    list_filter = ['unit']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Админка для договоров.
    """
    list_display = ['number', 'date', 'contractor', 'object', 'amount']
    list_filter = ['date', 'contractor', 'object']
    search_fields = ['number', 'contractor__name', 'object__name']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    """
    Админка для актов КС-2.
    """
    list_display = ['number', 'date', 'contract', 'object', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'date', 'contract', 'object']
    search_fields = ['number', 'contract__number', 'object__name']
    ordering = ['-date', '-number']
    date_hierarchy = 'date'
    inlines = [ActItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'date', 'contract', 'object', 'status')
        }),
        ('Период работ', {
            'fields': ('period_start', 'period_end')
        }),
        ('Финансовая информация', {
            'fields': ('total_amount', 'nds_amount', 'nds_rate', 'without_nds')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_by')
        }),
    )
    
    readonly_fields = ['total_amount', 'nds_amount', 'created_by', 'created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Автоматически заполняет поле created_by при создании."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ActItem)
class ActItemAdmin(admin.ModelAdmin):
    """
    Админка для строк актов.
    """
    list_display = ['number', 'name', 'act', 'quantity', 'price', 'total']
    list_filter = ['act', 'work_type']
    search_fields = ['name', 'act__number']
    ordering = ['act', 'number']
