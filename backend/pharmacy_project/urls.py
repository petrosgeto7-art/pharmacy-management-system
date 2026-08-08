"""pharmacy_project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls_auth')),
    path('api/users/', include('accounts.urls_users')),
    path('api/medicines/', include('medicines.urls')),
    path('api/categories/', include('medicines.urls_categories')),
    path('api/manufacturers/', include('medicines.urls_manufacturers')),
    path('api/inventory/', include('inventory.urls')),
    path('api/batches/', include('inventory.urls_batches')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/purchases/', include('purchases.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/returns/', include('returns.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/audit-logs/', include('audit.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
