from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReturnViewSet

router = DefaultRouter()
router.register(r'', ReturnViewSet, basename='returns')

urlpatterns = [
    path('', include(router.urls)),
]
