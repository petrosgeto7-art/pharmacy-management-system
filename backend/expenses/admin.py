from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_number', 'category', 'amount', 'payment_method', 'date', 'created_by')
    list_filter = ('category', 'payment_method')
    search_fields = ('expense_number', 'description')
    ordering = ('-date',)
    date_hierarchy = 'date'
