from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockMovementViewSet

router = DefaultRouter()
router.register(r'movements', StockMovementViewSet, basename='stock_movements')

urlpatterns = [
    path('', include(router.urls)),
]
