from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'category', 'description', 'amount', 'date', 'payment_method']
    list_filter = ['category', 'payment_method', 'date']
    search_fields = ['expense_number', 'description']
    date_hierarchy = 'date'
