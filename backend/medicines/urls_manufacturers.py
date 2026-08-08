from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewSet

router = DefaultRouter()
router.register(r'', ManufacturerViewSet, basename='manufacturers')

urlpatterns = [
    path('', include(router.urls)),
]
