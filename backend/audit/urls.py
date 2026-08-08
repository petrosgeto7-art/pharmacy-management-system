from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet

router = DefaultRouter()
router.register(r'', AuditLogViewSet, basename='audit_logs')

urlpatterns = [
    path('', include(router.urls)),
]
