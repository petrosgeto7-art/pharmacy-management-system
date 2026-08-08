from django.contrib import admin
from .models import Pharmacy


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'license_number')
    search_fields = ('name', 'license_number')
