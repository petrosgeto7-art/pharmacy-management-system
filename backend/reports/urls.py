from django.urls import path
from .views import SalesReportView, FinancialReportView

urlpatterns = [
    path('sales/', SalesReportView.as_view(), name='report_sales'),
    path('financial/', FinancialReportView.as_view(), name='report_financial'),
]
