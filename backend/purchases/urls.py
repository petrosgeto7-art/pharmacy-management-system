from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet

router = DefaultRouter()
router.register(r'', PurchaseViewSet, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
]
