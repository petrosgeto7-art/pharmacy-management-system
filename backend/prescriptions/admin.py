from django.contrib import admin
from .models import Prescription, PrescriptionItem

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_number', 'customer', 'doctor_name', 'prescription_date', 'status']
    list_filter = ['status', 'prescription_date']
    search_fields = ['prescription_number', 'customer__name', 'doctor_name']
    inlines = [PrescriptionItemInline]
    date_hierarchy = 'prescription_date'
