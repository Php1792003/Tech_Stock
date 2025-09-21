from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesInvoiceViewSet

router = DefaultRouter()
router.register(r'invoices', SalesInvoiceViewSet, basename='sales-invoice')

urlpatterns = [
    path('', include(router.urls)),
]