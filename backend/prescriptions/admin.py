from django.contrib import admin
from .models import Prescription, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 0


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_number', 'customer', 'doctor_name', 'status', 'prescription_date', 'dispensed_by')
    list_filter = ('status',)
    search_fields = ('prescription_number', 'customer__name', 'doctor_name')
    ordering = ('-prescription_date',)
    inlines = [PrescriptionItemInline]
