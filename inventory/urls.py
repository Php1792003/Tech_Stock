# inventory/urls.py (PHIÊN BẢN HOÀN CHỈNH)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, InventoryTxnViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'txns', InventoryTxnViewSet, basename='inventory-txn')

urlpatterns = [
    path('', include(router.urls)),
]